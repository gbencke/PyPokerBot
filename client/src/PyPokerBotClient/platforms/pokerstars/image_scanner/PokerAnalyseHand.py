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
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.platforms.utils import create_list_boolean_with_number_seats
from PyPokerBotClient.platforms.utils import create_list_string_with_number_seats
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


class PokerAnalyseHand:

    def get_flop_cards(self, analisys):
        return "".join([analisys['flop'][x] for x in range(self.FlopSize)])

    def analyse_hand_phase(self, analisys):
        number_cards_on_flop = len(self.get_flop_cards(analisys)) / 2
        if number_cards_on_flop == 0:
            return 'PREFLOP'
        else:
            return 'FLOP{}'.format(number_cards_on_flop)

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

    def send_hands_to_server(self, pocket_cards, flop_cards):
        command_to_send = '{} {}'.format(pocket_cards, flop_cards)
        # logging.debug('Sent to server:' + command_to_send[:30])
        r = requests.post(Settings.get_calculate_url(), json={"command": command_to_send})
        # logging.debug('Received from server:' + str(r.content)[:30])
        if r.status_code == 200:
            return command_to_send, ast.literal_eval(r.content)
        else:
            return command_to_send, ''

    def __init__(self, Platform, TableType, NumberOfSeats, FlopSize):
        self.Platform = Platform
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.FlopSize = FlopSize
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)

