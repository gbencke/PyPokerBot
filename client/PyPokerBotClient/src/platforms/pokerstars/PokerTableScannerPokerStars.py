import logging
import os
import numpy
import cv2
import ast
import datetime
import subprocess
import requests
from time import sleep
from datetime import datetime
from settings import settings
from model.PokerTableScanner import PokerTableScanner
from platforms.utils import get_histogram_from_image
from osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from custom_exceptions.NeedToSpecifySeatsException import NeedToSpecifySeatsException
from custom_exceptions.NeedToSpecifyTableTypeException import NeedToSpecifyTableTypeException


class PokerTableScannerPokerStars(PokerTableScanner):
    def create_list_none_with_number_seats(self):
        return [None for _ in range(self.NumberOfSeats)]

    def create_list_boolean_with_number_seats(self):
        return [False] * self.NumberOfSeats

    def create_list_string_with_number_seats(self):
        return [''] * self.NumberOfSeats

    def __init__(self, TableType=None, NumberOfSeats=None):
        self.Platform = 'POKERSTARS'
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None
        self.button_template_histogram = self.create_list_none_with_number_seats()
        self.player_button_threshold = None
        self.flop_has_card_histogram = self.create_list_none_with_number_seats()
        self.flop_has_card_threshold = None

    def set_table_type(self, table_type):
        self.TableType = table_type

    def set_number_of_seats(self, number_of_seats):
        self.NumberOfSeats = number_of_seats

    def get_player_hasbutton_histogram(self, index):
        if self.button_template_histogram[index] is None:
            self.button_template_histogram[index] = get_histogram_from_image(
                grab_image_from_file(
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER']['TEMPLATES_FOLDER'] + \
                    '\\' + 'BUTTON{}_TEMPLATE'.format(index + 1) + '.jpg'))
        return self.button_template_histogram[index]

    def get_player_hascard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER']['PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']))
        return self.player_has_card_histogram

    def get_player_has_card_threshold(self):
        if self.player_has_card_threshold is None:
            self.player_has_card_threshold = \
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['PLAY_HASCARD_THRESHOLD']
        return self.player_has_card_threshold

    def get_player_button_threshold(self):
        if self.player_button_threshold is None:
            self.player_button_threshold = \
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON_THRESHOLD']
        return self.player_button_threshold

    def get_player_has_card_in_position_histogram(self, index, Image):
        return \
            get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                        'PLAYER{}_HASCARD'.format(index + 1)],
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['PLAYERHASCARD_SIZE']))

    def analyse_players_with_cards(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for current_seat_index in range(self.NumberOfSeats):
            res = cv2.compareHist(
                self.get_player_hascard_histogram(),
                self.get_player_has_card_in_position_histogram(current_seat_index, Image), 0)
            ret[current_seat_index] = True if res > self.get_player_has_card_threshold() else False
        return ret

    def analyse_button(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for index in range(self.NumberOfSeats):
            current_seat_cv2_hist = get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON{}'.format(index + 1)],
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON_SIZE']))
            res = cv2.compareHist(self.get_player_hasbutton_histogram(index), current_seat_cv2_hist, 0)
            button_threshold = settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BUTTON_THRESHOLD']
            ret[index] = True if res > button_threshold else False
        return ret

    def get_flop_hascard_histogram(self, index):
        if self.flop_has_card_histogram[index] is None:
            self.flop_has_card_histogram[index] = get_histogram_from_image(
                grab_image_from_file(
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                        'FLOPCARD_HAS_NOCARD_TEMPLATE']))
        return self.flop_has_card_histogram[index]

    def get_flop_has_card_threshold(self):
        if self.flop_has_card_histogram is None:
            self.flop_has_card_histogram = \
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['PLAY_HASCARD_THRESHOLD']
        return self.flop_has_card_histogram

    def check_if_flop_pos_is_empty(self, Image, index):
        template_flop_empty_cv2_hist = self.get_flop_hascard_histogram(index)
        template_flop_pos1 = \
            get_histogram_from_image(grab_image_pos_from_image(
                Image,
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['FLOPCARD{}'.format(index + 1)],
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['FLOPCARD_SIZE']))
        res = cv2.compareHist(template_flop_empty_cv2_hist, template_flop_pos1, 0)
        if res > self.get_flop_has_card_threshold():
            return True
        else:
            return False

    def get_card_in_flop_pos_is_empty(self, Image, index):
        flop_card_key = 'FLOPCARD{}'.format(index + 1)
        image_from_flop_card = grab_image_pos_from_image(
            Image,
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][flop_card_key],
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['FLOPCARD_SIZE'])
        return image_from_flop_card, numpy.array(image_from_flop_card)[:, :, ::-1].copy()

    def get_card_template(self, current_card, current_suit):
        filename = settings['PLATFORMS'][self.Platform]['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + \
                   current_card + current_suit + '.jpg'
        Image_template = grab_image_from_file(filename)
        return Image_template, numpy.array(Image_template)[:, :, ::-1].copy()

    def analyse_flop_template(self, Image):
        ret = self.create_list_string_with_number_seats()
        for index in range(self.NumberOfSeats):
            if not self.check_if_flop_pos_is_empty(Image, index):
                return ret
            selected_card = ''
            selected_card_res = 1000000000
            image_from_flop_card, current_flop_image = self.get_card_in_flop_pos_is_empty(Image, index)
            for current_suit in PokerTableScanner.suits:
                for current_card in PokerTableScanner.cards:
                    template_image, current_card_image = self.get_card_template(current_card, current_suit)
                    res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                    if res < selected_card_res:
                        selected_card = current_card + current_suit
                        selected_card_res = res
            correct_suit = self.get_suite_from_image(image_from_flop_card)
            if correct_suit != selected_card[1]:
                selected_card = selected_card[0] + correct_suit
            ret[index] = selected_card
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
        if button[hero_pos]:
            return 'BUTTON'
        current_pos_analysed = hero_pos + 1
        while True:
            if current_pos_analysed > 6:
                current_pos_analysed = 1
            if cards[current_pos_analysed]:
                return ''
            if button[current_pos_analysed]:
                return 'BUTTON'
            current_pos_analysed += 1

    def get_hero_card_image(self, Image, seat, current_hero_card):
        flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
        image_from_player = grab_image_pos_from_image(
            Image,
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][flop_card_key],
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['FLOPCARD_SIZE'])
        current_flop_image = numpy.array(image_from_player)[:, :, ::-1].copy()
        return image_from_player, current_flop_image

    def analyse_hero(self, im, cards, nocards, button):
        ret = {'HERO_CARDS': '', 'POSITION': ''}
        for seat in range(self.NumberOfSeats):
            if cards[seat] == False and nocards[seat] == False:
                ret['HERO_POS'] = seat + 1
                for current_hero_card in range(2):
                    selected_card = ''
                    selected_card_res = 1000000000
                    image_from_player, current_flop_image = self.get_hero_card_image(im, seat, current_hero_card)
                    for current_suit in PokerTableScanner.suits:
                        for current_card in PokerTableScanner.cards:
                            template_image, current_card_image = self.get_card_template(current_card, current_suit)
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

    def get_player_hasnocard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                        'PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']))
        return self.player_has_card_histogram

    def analyse_players_without_cards(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for index in range(self.NumberOfSeats):
            empty_card_key = settings['PLATFORMS'][self.Platform]['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + \
                             'PLAYER{}_HASNOCARD'.format(index + 1) + '.jpg'
            empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))

            current_pos_key = 'PLAYER{}_HASCARD'.format(index + 1)
            current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
                Image,
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][current_pos_key],
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['PLAYERHASCARD_SIZE']))
            res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
            ret[index] = True if res > \
                                 settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                                     'PLAY_HASCARD_THRESHOLD'] \
                else False
        return ret

    def analyse_commands(self, im):
        ret = ['', '', '']

        for x in range(3):
            current_command = x + 1

            template_has_command_cv2_hist = \
                get_histogram_from_image(
                    grab_image_from_file(
                        settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType] \
                            ['COMMAND_TEST_TEMPLATE{}'.format(current_command)]))

            has_command_cv2_hist = \
                get_histogram_from_image(grab_image_pos_from_image(
                    im,
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                        'COMMAND_POS{}'.format(current_command)],
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['COMMAND_TEST_SIZE']))
            res = cv2.compareHist(template_has_command_cv2_hist, has_command_cv2_hist, 0)
            if res > settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['COMMAND_TEST_TOLERANCE']:
                im_command = grab_image_pos_from_image(
                    im,
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType][
                        'COMMAND_POS{}'.format(current_command)],
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['COMMAND_SIZE']
                )
                command_image_name = 'command{}.jpg'.format(current_command)
                im_command.save(command_image_name)
                return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                                shell=False)
                if len(return_from_tesseract.strip()) == 0:
                    error_filename = command_image_name + '.error.' + datetime.now().strftime(
                        "%Y%m%d%H%M%S.%f") + '.jpg'
                    logging.debug("ERROR ON TESSERACT!!! " + error_filename)
                    im_command.save(error_filename)
                ret[x] = return_from_tesseract.replace('\r\n', ' ').replace('  ', ' ')
                os.remove(command_image_name)
                sleep(0.2)
        return ret

    def analyse_hand_phase(self, analisys):
        return 'PREFLOP' if len(self.get_flop_cards(analisys)) == 0 else 'FLOP'

    def get_flop_cards(self, analisys):
        return "".join([analisys['flop'][x] for x in range(5)])

    def send_hands_to_server(self, pocket_cards, flop_cards):
        command_to_send = '{} {}'.format(pocket_cards + ':XX', flop_cards)
        logging.debug('Sent to server:' + command_to_send[:30])
        r = requests.post(settings['STRATEGIES']['SIMPLE']['CALCULATE_URL'], json={"command": command_to_send})
        logging.debug('Received from server:' + str(r.content)[:30])
        if r.status_code == 200:
            return command_to_send, ast.literal_eval(r.content)
        else:
            return command_to_send, ''

    def analyse_hand(self, analisys):
        ret = {}
        if len(analisys['hero']['HERO_CARDS']) == 0:
            return ret
        flop_cards = self.get_flop_cards(analisys)
        ret['HAND_PHASE'] = self.analyse_hand_phase(analisys)
        command, result = self.send_hands_to_server(analisys['hero']['HERO_CARDS'], flop_cards)
        ret['RESULT'] = result
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
        result['hero'] = self.analyse_hero(im, result['cards'], result['nocards'], result['button'])
        result['commands'] = self.analyse_commands(im)
        result['hand_analisys'] = self.analyse_hand(result)
        return result
