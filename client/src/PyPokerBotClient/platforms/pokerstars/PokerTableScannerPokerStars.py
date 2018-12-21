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
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from PyPokerBotClient.custom_exceptions.NeedToSpecifySeatsException import NeedToSpecifySeatsException
from PyPokerBotClient.custom_exceptions.NeedToSpecifyTableTypeException import NeedToSpecifyTableTypeException
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalysePlayersWithCards import PokerAnalysePlayersWithCards
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseCommands import PokerAnalyseCommands


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
        self.FlopSize = 5
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None
        self.button_template_histogram = self.create_list_none_with_number_seats()
        self.player_button_threshold = None
        self.flop_has_card_histogram = self.create_list_none_with_number_seats()
        self.flop_has_card_threshold = None
        self.non_decimal = re.compile(r'[^\d.]+')
        self.AnalyseCommands = PokerAnalyseCommands(self.Platform, self.TableType)
        self.AnalysePlayersWithCards = PokerAnalysePlayersWithCards()

    def set_table_type(self, table_type):
        self.TableType = table_type

    def set_number_of_seats(self, number_of_seats):
        self.NumberOfSeats = number_of_seats

    def get_player_hasbutton_histogram(self, index):
        if self.button_template_histogram[index] is None:
            self.button_template_histogram[index] = get_histogram_from_image(
                grab_image_from_file(Settings.get_button_template_file(self.Platform, self.TableType, index)))
        return self.button_template_histogram[index]

    def get_player_hascard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_player_has_unknown_card_template(self.Platform)))
        return self.player_has_card_histogram

    def get_player_has_card_threshold(self):
        if self.player_has_card_threshold is None:
            self.player_has_card_threshold = Settings.get_play_hascard_threshold(self.Platform, self.TableType)
        return self.player_has_card_threshold

    def get_player_button_threshold(self):
        if self.player_button_threshold is None:
            self.player_button_threshold = Settings.get_button_threshold(self.Platform, self.TableType)
        return self.player_button_threshold

    def get_player_has_card_in_position_histogram(self, index, Image):
        return \
            get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    Settings.get_player_hascard(self.Platform, self.TableType, index),
                    Settings.get_playerhascard_size(self.Platform, self.TableType)))

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
                    Settings.get_button_template(self.Platform, self.TableType, index),
                    Settings.get_button_size(self.Platform, self.TableType)))
            res = cv2.compareHist(self.get_player_hasbutton_histogram(index), current_seat_cv2_hist, 0)
            button_threshold = Settings.get_button_threshold(self.Platform, self.TableType)
            ret[index] = True if res > button_threshold else False
        return ret

    def get_flop_hascard_histogram(self, index):
        if self.flop_has_card_histogram[index] is None:
            self.flop_has_card_histogram[index] = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_flop_has_nocard_template(self.Platform, self.TableType)))
        return self.flop_has_card_histogram[index]

    def get_flop_has_card_threshold(self):
        if self.flop_has_card_threshold is None:
            self.flop_has_card_threshold = \
                Settings.get_play_hascard_threshold(self.Platform, self.TableType)
        return self.flop_has_card_threshold

    def check_if_flop_pos_is_empty(self, Image, index):
        template_flop_empty_cv2_hist = self.get_flop_hascard_histogram(index)
        template_flop_pos1 = \
            get_histogram_from_image(grab_image_pos_from_image(
                Image,
                Settings.get_flopcard(self.Platform, self.TableType, index),
                Settings.get_flopcard_size(self.Platform, self.TableType)))
        res = cv2.compareHist(template_flop_empty_cv2_hist, template_flop_pos1, 0)
        if res > self.get_flop_has_card_threshold():
            return True
        else:
            return False

    def get_card_in_flop_pos_is_empty(self, Image, index):
        flop_card_key = 'FLOPCARD{}'.format(index + 1)
        image_from_flop_card = grab_image_pos_from_image(
            Image,
            Settings.get_flop_card_key(self.Platform, self.TableType, flop_card_key ),
            Settings.get_flopcard_size(self.Platform, self.TableType))
        return image_from_flop_card, numpy.array(image_from_flop_card)[:, :, ::-1].copy()

    def get_card_template(self, current_card, current_suit):
        filename = Settings.get_card_template(self.Platform, current_card, current_suit)
        Image_template = grab_image_from_file(filename)
        return Image_template, numpy.array(Image_template)[:, :, ::-1].copy()

    def analyse_flop_template(self, Image):
        ret = self.create_list_string_with_number_seats()
        for index in range(self.FlopSize):
            if self.check_if_flop_pos_is_empty(Image, index):
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

    def get_absoulute_hero_pos(self, hero_pos, button):
        if len([x for x in button if x == True]) == 0:
            return 'MP'
        distance = 0
        current_pos_analysed = hero_pos
        while True:
            distance += 1
            if current_pos_analysed == self.NumberOfSeats:
                current_pos_analysed = 0
            if button[current_pos_analysed]:
                break
            current_pos_analysed += 1
        if distance == 0:
            return 'BUTTON'
        if distance == 1:
            return 'LP'
        if distance == 2:
            return 'MP'
        if distance == 3:
            return 'MP'
        if distance == 4:
            return 'BB'
        if distance == 5:
            return 'SB'

    def get_hero_position(self, hero_pos, cards, button):
        loop_total = 0
        if button[hero_pos - 1]:
            return 'BUTTON'
        current_pos_analysed = hero_pos
        while True:
            loop_total += 1
            if current_pos_analysed == self.NumberOfSeats:
                current_pos_analysed = 0
            if cards[current_pos_analysed] or loop_total > 3:
                return self.get_absoulute_hero_pos(hero_pos, button)
            if button[current_pos_analysed]:
                return 'BUTTON'
            current_pos_analysed += 1

    def get_hero_card_image(self, Image, seat, current_hero_card):
        flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
        image_from_player = grab_image_pos_from_image(
            Image,
            Settings.get_flop_card_key(self.Platform, self.TableType, flop_card_key),
            Settings.get_flopcard_size(self.Platform, self.TableType))
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
                    Settings.get_player_has_unknown_card_template(self.Platform)))
        return self.player_has_card_histogram

    def analyse_players_without_cards(self, Image):
        ret = self.create_list_boolean_with_number_seats()
        for index in range(self.NumberOfSeats):
            empty_card_key = Settings.get_player_hasnocard_template(self.Platform, index)
            empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))

            current_pos_key = 'PLAYER{}_HASCARD'.format(index + 1)
            current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
                Image,
                Settings.get_command_current_pos_key(self.Platform, self.TableType, current_pos_key),
                Settings.get_playerhascard_size(self.Platform, self.TableType)))
            res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
            ret[index] = True if res > Settings.get_play_hascard_threshold(self.Platform, self.TableType) else False
        return ret


    def check_for_button_template(self, im, template, pos):
        template_has_command_cv2_hist = \
            get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_template(self.Platform, self.TableType, template)))

        has_command_cv2_hist = \
            get_histogram_from_image(grab_image_pos_from_image(
                im,
                Settings.get_command_pos(self.Platform, self.TableType, pos),
                Settings.get_command_test_size(self.Platform, self.TableType)))

        res = cv2.compareHist(template_has_command_cv2_hist, has_command_cv2_hist, 0)
        if res > Settings.get_command_test_tolerance(self.Platform, self.TableType):
            return True, (template, 0, template)

    def check_for_check_button(self, im):
        return self.check_for_button_template(im, 'CHECK', 1)

    def check_for_fold_button(self, im):
        return self.check_for_button_template(im, 'FOLD', 0)


    def analyse_hand_phase(self, analisys):
        number_cards_on_flop = len(self.get_flop_cards(analisys)) / 2
        if number_cards_on_flop == 0:
            return 'PREFLOP'
        else:
            return 'FLOP{}'.format(number_cards_on_flop)

    def get_flop_cards(self, analisys):
        return "".join([analisys['flop'][x] for x in range(self.FlopSize)])

    def send_hands_to_server(self, pocket_cards, flop_cards):
        command_to_send = '{} {}'.format(pocket_cards, flop_cards)
        # logging.debug('Sent to server:' + command_to_send[:30])
        r = requests.post(Settings.get_calculate_url(), json={"command": command_to_send})
        # logging.debug('Received from server:' + str(r.content)[:30])
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
        if ret['hand_phase'] == 'PREFLOP':
            pocket_cards_to_server = analisys['hero']['hero_cards'] + ":XX"
        else:
            total_villains = len([x for x in analisys['cards'] if x == True])
            # We don't have performance for more than 2 villains so...
            total_villains = 2 if total_villains > 2 else total_villains
            pocket_cards_to_server = analisys['hero']['hero_cards'] + ":" + ":".join(['XX'] * total_villains)

        command, result = self.send_hands_to_server(pocket_cards_to_server, flop_cards)
        ret['result'] = result
        return ret

    def analyse_pot(self, im):
        im_command = grab_image_pos_from_image(
            im,
            Settings.get_pot(self.Platform, self.TableType),
            Settings.get_pot_size(self.Platform, self.TableType))
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

    def check_if_bet_is_present(self, index, im):
        player_has_bet_histogram = get_histogram_from_image(
            grab_image_pos_from_image(im, Settings.get_bet(self.Platform, self.TableType, index),
                                      Settings.get_bet_size(self.Platform, self.TableType)))
        nobet_histogram = get_histogram_from_image(
            grab_image_from_file(Settings.get_nobet_template(self.Platform, self.TableType)))

        res = cv2.compareHist(player_has_bet_histogram, nobet_histogram, 0)
        if res > 0.9:
            return False
        else:
            return True

    def analyse_bets(self, im):
        returned_list = self.create_list_none_with_number_seats()
        for x in range(self.NumberOfSeats):
            if not self.check_if_bet_is_present(x, im):
                continue
            im_command = grab_image_pos_from_image(
                im,
                Settings.get_bet(self.Platform, self.TableType, x),
                Settings.get_bet_size(self.Platform, self.TableType)
            )
            command_image_name = 'command_bet.jpg'
            im_command.save(command_image_name)
            start, stop, step = self.get_offset_for_numbers(im_command, x in [0, 1, 2])
            for test in range(start, stop, step):
                coords = Settings.get_bet(self.Platform, self.TableType, x)
                if x in [0, 1, 2]:
                    coords = (coords[0] - (test * 1), coords[1])
                else:
                    coords = (coords[0] + (test * 1), coords[1])
                im_command = grab_image_pos_from_image(
                    im,
                    coords,
                    Settings.get_bet_size(self.Platform, self.TableType, x)
                )
                command_image_name = 'command_bet.jpg'
                im_command.save(command_image_name)
                return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                                shell=False)
                return_from_tesseract = return_from_tesseract.replace('$11', '$0.')
                if len(return_from_tesseract) == 0:
                    break
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

    def has_command_to_execute(self, analisys):
        return has_command_to_execute(analisys)

    def analyze_from_image(self, im):
        if self.NumberOfSeats is None:
            raise NeedToSpecifySeatsException('You need to specify the number of seats prior to start analisys')
        if self.TableType is None:
            raise NeedToSpecifyTableTypeException('You need to specify the table type prior to start analisys')
        result = {}
        result['seats'] = self.NumberOfSeats
        result['commands'] = self.AnalyseCommands.analyse_commands(im)
        result['cards'] = self.analyse_players_with_cards(im)
        result['nocards'] = self.analyse_players_without_cards(im)
        result['button'] = self.analyse_button(im)
        result['flop'] = self.analyse_flop_template(im)
        if has_command_to_execute(result):
            result['hero'] = self.analyse_hero(im, result['cards'], result['nocards'], result['button'])
            result['hand_analisys'] = self.analyse_hand(result)
        return result
