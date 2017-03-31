import logging
import os
import numpy
import cv2
import ast
import datetime
import subprocess
import requests
import re
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

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        PokerTableScanner.__init__(self, TableType, NumberOfSeats, BB, SB)
        self.Platform = 'POKERSTARS'
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None
        self.button_template_histogram = self.create_list_none_with_number_seats()
        self.player_button_threshold = None
        self.flop_has_card_histogram = self.create_list_none_with_number_seats()
        self.flop_has_card_threshold = None
        self.non_decimal = re.compile(r'[^\d.]+')

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

    def get_hero_position(self, hero_pos, cards, button):
        if button[hero_pos]:
            return 'BUTTON'
        current_pos_analysed = hero_pos + 1
        while True:
            if current_pos_analysed == self.NumberOfSeats:
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
        ret = {'hero_cards': '', 'position': ''}
        for seat in range(self.NumberOfSeats):
            if cards[seat] == False and nocards[seat] == False:
                ret['hero_pos'] = seat + 1
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
                    ret['hero_cards'] += selected_card
                break
        hero_position = ''
        if 'hero_pos' in ret:
            hero_position = self.get_hero_position(ret['hero_pos'], cards, button)
        ret['position'] = hero_position
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

    def generate_command_tuple(self, str):
        command = ''
        value = ''
        if 'FOLD' in str.upper():
            command = 'FOLD'
        if 'RAISE' in str.upper():
            command = 'RAISE'
        if 'CHECK' in str.upper():
            command = 'CHECK'
        if 'CALL' in str.upper():
            command = 'CALL'
        if '$' in str:
            value = str.split('$')[1].strip()
            value = float(value) / self.BB
        return (command, value, str)


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
                ret[x] = self.generate_command_tuple(return_from_tesseract.replace('\r\n', ' ').replace('  ', ' '))
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
        if len(analisys['hero']['hero_cards']) == 0:
            return ret
        flop_cards = self.get_flop_cards(analisys)
        ret['hand_phase'] = self.analyse_hand_phase(analisys)
        command, result = self.send_hands_to_server(analisys['hero']['hero_cards'], flop_cards)
        ret['result'] = result
        return ret

    def analyse_pot(self, im):
        im_command = grab_image_pos_from_image(
            im,
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['POT'],
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['POT_SIZE']
        )
        command_image_name = 'command_pot.jpg'
        im_command.save(command_image_name)
        return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                        shell=False)
        if len(return_from_tesseract.strip()) == 0:
            error_filename = command_image_name + '.error.' + datetime.now().strftime(
                "%Y%m%d%H%M%S.%f") + '.jpg'
            logging.debug("ERROR ON TESSERACT!!! " + error_filename)
            im_command.save(error_filename)
        os.remove(command_image_name)
        sleep(0.2)
        ret = return_from_tesseract.replace('\r', '').replace('\n', '').replace(' ', '')
        returned_string = ret
        ret = ret.split("$")[1]
        ret = float(ret) / self.BB
        return ret, returned_string

    def check_if_bet_is_present(self,index, im):
        player_has_bet_histogram = get_histogram_from_image(grab_image_pos_from_image(im,
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET{}'.format(index + 1)],
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET_SIZE']))
        nobet_histogram = get_histogram_from_image(grab_image_from_file(
            settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['NOBET_TEMPLATE']))
        res = cv2.compareHist(player_has_bet_histogram, nobet_histogram, 0)
        if res > 0.9:
            return False
        else:
            return True

    def analyse_bets(self, im):
        returned_list = self.create_list_none_with_number_seats()
        for x in range(self.NumberOfSeats):
            if not self.check_if_bet_is_present(x,im):
                continue
            im_command = grab_image_pos_from_image(
                im,
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET{}'.format(x + 1)],
                settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET_SIZE']
            )
            command_image_name = 'command_bet.jpg'
            im_command.save(command_image_name)
            start, stop, step = self.get_offset_for_numbers(im_command, x in [0, 1, 2])
            for test in range(start, stop, step):
                coords = settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET{}'.format(x + 1)]
                if x in [0, 1, 2]:
                    coords = (coords[0] - (test * 1), coords[1])
                else:
                    coords = (coords[0] + (test * 1), coords[1])
                im_command = grab_image_pos_from_image(
                    im,
                    coords,
                    settings['PLATFORMS'][self.Platform]['TABLE_SCANNER'][self.TableType]['BET_SIZE']
                )
                command_image_name = 'command_bet.jpg'
                im_command.save(command_image_name)
                return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                                shell=False)
                return_from_tesseract = return_from_tesseract.replace('$11','$0.')
                if len(return_from_tesseract) == 0:
                    break
                logging.debug(return_from_tesseract)
                if not (('$' in return_from_tesseract) and ('.' in return_from_tesseract)):
                    continue
                os.remove(command_image_name)
                ret = return_from_tesseract.replace('\r', '').replace('\n', '').replace(' ', '').replace('\'', '')
                ret = ret.split("$")[1]
                ret = self.non_decimal.sub('', ret)
                returned_string = ret
                ret = float(ret) / self.BB
                if ret > 200 or ret == 0:
                    continue
                returned_list[x] = (ret, returned_string, return_from_tesseract)
                break
        return returned_list

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
            'flop': self.analyse_flop_template(im),

        }
        pot, pot_str = self.analyse_pot(im)
        result['pot'] = (pot, pot_str)
        result['bet'] = self.analyse_bets(im)
        result['hero'] = self.analyse_hero(im, result['cards'], result['nocards'], result['button'])
        result['commands'] = self.analyse_commands(im)
        result['hand_analisys'] = self.analyse_hand(result)
        return result
