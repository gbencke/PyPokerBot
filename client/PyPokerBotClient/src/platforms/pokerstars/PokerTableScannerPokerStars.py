import numpy
import cv2
from settings import settings
from model.PokerTableScanner import PokerTableScanner
from platforms.utils import get_histogram_from_image
from osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from custom_exceptions.NeedToSpecifySeatsException import NeedToSpecifySeatsException
from custom_exceptions.NeedToSpecifyTableTypeException import NeedToSpecifyTableTypeException


class PokerTableScannerPokerStars(PokerTableScanner):
    def create_list_none_with_number_seats(self):
        return [None] * self.NumberOfSeats

    def create_list_boolean_with_number_seats(self):
        return [False] * self.NumberOfSeats

    def __init__(self, TableType=None, NumberOfSeats=None):
        self.Platform = 'POKERSTARS'
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None
        self.button_template_histogram = self.create_list_none_with_number_seats()
        self.player_button_threshold = None

    def set_table_type(self, table_type):
        self.TableType = table_type

    def set_number_of_seats(self, number_of_seats):
        self.NumberOfSeats = number_of_seats

    def get_player_hasbutton_histogram(self, index):
        if self.button_template_histogram[index] is None:
            self.button_template_histogram[index] = get_histogram_from_image(
                grab_image_pos_from_image(
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['TEMPLATES_FOLDER'] + \
                    '\\' + 'BUTTON{}_TEMPLATE'.format(index + 1) + '.jpg'))
        return self.button_template_histogram[index]

    def get_player_hascard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']))
        return self.player_has_card_histogram

    def get_player_has_card_threshold(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = \
                settings[self.Platform]['TABLE_SCANNER'][self.TableType]['PLAY_HASCARD_THRESHOLD']
        return self.player_has_card_histogram

    def get_player_button_threshold(self):
        if self.player_button_threshold is None:
            self.player_button_threshold = \
                settings[self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON_THRESHOLD']
        return self.player_button_threshold

    def get_player_has_card_in_position_histogram(self, index, Image):
        return \
            get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['PLAYER{}_HASCARD'.format(index + 1)],
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['PLAYERHASCARD_SIZE']))

    def analyse_players_with_cards(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for current_seat_index in range(self.NumberOfSeats):
            ret[current_seat_index] = True if \
                cv2.compareHist(
                    self.get_player_hascard_histogram(),
                    self.get_player_has_card_in_position_histogram(current_seat_index, Image), 0) > \
                self.get_player_has_card_threshold() else False
        return ret

    def analyse_button(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for index in range(self.NumberOfSeats):
            current_seat_cv2_hist = get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON{}'.format(index + 1)],
                    settings[self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON_SIZE']))
            res = cv2.compareHist(self.get_player_hasbutton_histogram(index), current_seat_cv2_hist, 0)
            ret[index] = True if res > settings['TABLE_SCANNER']['BUTTON_THRESHOLD'] else False
        return ret

    def analyse_flop_template(self, Image):
        ret = {}
        for current_flop_pos in range(5):
            template_flop_empty_cv2_hist = get_histogram_from_image(
                grab_image_from_file(settings['TABLE_SCANNER']['FLOPCARD_HAS_NOCARD_TEMPLATE']))
            template_flop_pos1 = \
                get_histogram_from_image(grab_image_pos_from_image(
                    Image,
                    settings['TABLE_SCANNER']['FLOPCARD{}'.format(current_flop_pos + 1)],
                    settings['TABLE_SCANNER']['FLOPCARD_SIZE']))
            res = cv2.compareHist(template_flop_empty_cv2_hist, template_flop_pos1, 0)
            if res > settings['TABLE_SCANNER']['PLAY_HASCARD_THRESHOLD']:
                return ret
            selected_card = ''
            selected_card_res = 1000000000
            flop_card_key = 'FLOPCARD{}'.format(current_flop_pos + 1)
            image_from_flop_card = grab_image_pos_from_image(
                Image,
                settings['TABLE_SCANNER'][flop_card_key],
                settings['TABLE_SCANNER']['FLOPCARD_SIZE'])
            current_flop_image = numpy.array(image_from_flop_card)[:, :, ::-1].copy()
            for current_suit in ['h', 's', 'c', 'd']:
                for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                    filename = settings['TABLE_SCANNER'][
                                   'TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                    current_card_image = numpy.array(grab_image_from_file(filename))[:, :, ::-1].copy()
                    res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                    # print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1, current_card + current_suit,res, selected_card))
                    if res < selected_card_res:
                        selected_card = current_card + current_suit
                        selected_card_res = res
            correct_suit = self.get_suite_from_image(image_from_flop_card)
            if correct_suit != selected_card[1]:
                selected_card = selected_card[0] + correct_suit
            ret[flop_card_key] = selected_card
        return ret

    def get_suite_from_image(self, selected_image):
        red = 0
        blue = 0
        green = 0
        black = 0
        for w in range(selected_image.width):
            for h in range(selected_image.height):
                pixel = selected_image.getpixel((w, h))
                if pixel[0] >= 230 and pixel[1] >= 230 and pixel[2] >= 230:
                    continue
                if pixel[0] < 20 and pixel[1] < 20 and pixel[2] < 20:
                    black += 1
                    continue
                if pixel[0] >= pixel[1] and pixel[0] >= pixel[2]:
                    red += 1
                    continue
                if pixel[1] >= pixel[0] and pixel[1] >= pixel[2]:
                    green += 1
                    continue
                if pixel[2] >= pixel[0] and pixel[2] >= pixel[1]:
                    blue += 1
                    continue
        # print("red:{} green:{} blue:{} black:{}".format(red, green, blue, black))
        if black > 200:
            return 's'
        if red > green and red > blue and red > black:
            return 'h'
        if green > red and green > blue and green > black:
            return 'c'
        if blue > red and blue > green and blue > black:
            return 'd'

    def get_hero_position(self, hero_pos, cards, button):
        if button['BUTTON{}'.format(hero_pos)] == 'BUTTON':
            return 'BUTTON'
        current_pos_analysed = hero_pos + 1
        while True:
            if current_pos_analysed > 6:
                current_pos_analysed = 1
            if cards['PLAYER{}_HASCARD'.format(current_pos_analysed)] == 'CARD':
                return ''
            if button['BUTTON{}'.format(current_pos_analysed)] == 'BUTTON':
                return 'BUTTON'
            current_pos_analysed += 1

    def analyse_hero(self, im, cards, nocards, button):
        ret = {}
        ret['HERO_CARDS'] = ''
        for seat in range(6):
            card_key = 'PLAYER{}_HASCARD'.format(seat + 1)
            nocard_key = 'NOCARD{}'.format(seat + 1)
            if len(cards[card_key]) == 0 and len(nocards[nocard_key]) == 0:
                # print("found hero at {}".format(seat + 1))
                ret['HERO_POS'] = seat + 1
                for current_hero_card in range(2):
                    selected_card = ''
                    selected_card_res = 1000000000
                    flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
                    image_from_player = grab_image_pos_from_image(
                        im,
                        settings['TABLE_SCANNER'][flop_card_key],
                        settings['TABLE_SCANNER']['FLOPCARD_SIZE'])
                    current_flop_image = numpy.array(image_from_player)[:, :, ::-1].copy()
                    for current_suit in ['h', 's', 'c', 'd']:
                        for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                            filename = settings['TABLE_SCANNER'][
                                           'TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                            image_from_file = grab_image_from_file(filename)
                            current_card_image = numpy.array(image_from_file)[:, :, ::-1].copy()
                            res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                            if res < selected_card_res:
                                selected_card = current_card + current_suit
                                selected_card_res = res
                    correct_suit = self.get_suite_from_image(image_from_player)
                    if correct_suit != selected_card[1]:
                        selected_card = selected_card[0] + correct_suit
                    ret['HERO_CARDS'] += selected_card
                break
        hero_position = ''
        if 'HERO_POS' in ret:
            hero_position = self.get_hero_position(ret['HERO_POS'], cards, button)
        ret['POSITION'] = hero_position
        return ret

    def analyse_players_without_cards(self, Image):
        ret = {}
        for current_seat_index in range(6):
            empty_card_key = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + 'PLAYER{}_HASNOCARD'.format(
                current_seat_index + 1) + '.jpg'
            empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))
            current_pos_key = 'PLAYER{}_HASCARD'.format(current_seat_index + 1)
            current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
                Image, settings['TABLE_SCANNER'][current_pos_key],
                settings['TABLE_SCANNER']['PLAYERHASCARD_SIZE']))
            res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
            ret['NOCARD{}'.format(current_seat_index + 1)] = 'NOCARD' if res > settings['TABLE_SCANNER'][
                'PLAY_HASCARD_THRESHOLD'] else ''
        return ret

    def analyze_from_image(self, im):
        if self.NumberOfSeats is None:
            raise NeedToSpecifySeatsException('You need to specify the number of seats prior to start analisys')
        if self.TableType is None:
            raise NeedToSpecifyTableTypeException('You need to specify the table type prior to start analisys')
        result = {
            'seats': self.NumberOfSeats,
            'cards': self.analyse_players_with_cards(im),
            'nocards': self.analyse_players_without_cards(im),
            'button': self.analyse_button(im),
            'flop': self.analyse_flop_template(im)
        }
        result['hero'] = self.analyse_hero(im, result['cards'], result['nocards'], result['button']),
        return result
