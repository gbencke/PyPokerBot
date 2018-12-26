# coding=utf-8
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
from PyPokerBotClient.platforms.utils import get_card_template
from PyPokerBotClient.platforms.utils import get_suite_from_image
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from PyPokerBotClient.custom_exceptions.NeedToSpecifySeatsException import NeedToSpecifySeatsException
from PyPokerBotClient.custom_exceptions.NeedToSpecifyTableTypeException import NeedToSpecifyTableTypeException
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalysePlayersWithCards import \
    PokerAnalysePlayersWithCards
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalysePlayersWithoutCards import \
    PokerAnalysePlayersWithoutCards
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseCommands import PokerAnalyseCommands
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseButton import PokerAnalyseButton
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseFlop import PokerAnalyseFlop
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseHero import PokerAnalyseHero


class PokerTableScannerPokerStars(PokerTableScanner):

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        PokerTableScanner.__init__(self, TableType, NumberOfSeats, BB, SB)
        self.Platform = 'POKERSTARS'
        self.FlopSize = 5
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.player_button_threshold = None
        self.non_decimal = re.compile(r'[^\d.]+')
        self.AnalyseCommands = PokerAnalyseCommands(self.Platform, self.TableType)
        self.AnalysePlayersWithCards = PokerAnalysePlayersWithCards(self.Platform, self.TableType, self.NumberOfSeats)
        self.AnalysePlayersWithoutCards = PokerAnalysePlayersWithoutCards(self.Platform, self.TableType,
                                                                          self.NumberOfSeats)
        self.AnalyseButton = PokerAnalyseButton(self.Platform, self.TableType, self.NumberOfSeats)
        self.AnalyseFlop = PokerAnalyseFlop(self.Platform, self.TableType, self.NumberOfSeats, self.FlopSize)
        self.AnalyseHero = PokerAnalyseHero(self.Platform, self.TableType, self.NumberOfSeats)

    def set_table_type(self, table_type):
        self.TableType = table_type

    def set_number_of_seats(self, number_of_seats):
        self.NumberOfSeats = number_of_seats

    def get_player_button_threshold(self):
        if self.player_button_threshold is None:
            self.player_button_threshold = Settings.get_button_threshold(self.Platform, self.TableType)
        return self.player_button_threshold



    def get_player_hasnocard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_player_has_unknown_card_template(self.Platform)))
        return self.player_has_card_histogram

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
        returned_list = create_list_none_with_number_seats()
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
        result['cards'] = self.AnalysePlayersWithCards.analyse_players_with_cards(im)
        result['nocards'] = self.AnalysePlayersWithoutCards.analyse_players_without_cards(im)
        result['button'] = self.AnalyseButton.analyse_button(im)
        result['flop'] = self.AnalyseFlop.analyse_flop_template(im)
        if has_command_to_execute(result):
            result['hero'] = self.AnalyseHero.analyse_hero(im, result['cards'], result['nocards'], result['button'])
            result['hand_analisys'] = self.analyse_hand(result)
        return result
