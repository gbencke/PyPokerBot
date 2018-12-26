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
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseHand import PokerAnalyseHand


class PokerTableScannerPokerStars(PokerTableScanner):

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        PokerTableScanner.__init__(self, TableType, NumberOfSeats, BB, SB)
        self.Platform = 'POKERSTARS'
        self.FlopSize = 5
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.player_button_threshold = None
        self.non_decimal = re.compile(r'[^\d.]+')
        self.AnalyseCommands = PokerAnalyseCommands(self.Platform, self.TableType, self.BB)
        self.AnalysePlayersWithCards = PokerAnalysePlayersWithCards(self.Platform, self.TableType, self.NumberOfSeats)
        self.AnalysePlayersWithoutCards = PokerAnalysePlayersWithoutCards(self.Platform, self.TableType,
                                                                          self.NumberOfSeats)
        self.AnalyseButton = PokerAnalyseButton(self.Platform, self.TableType, self.NumberOfSeats)
        self.AnalyseFlop = PokerAnalyseFlop(self.Platform, self.TableType, self.NumberOfSeats, self.FlopSize)
        self.AnalyseHero = PokerAnalyseHero(self.Platform, self.TableType, self.NumberOfSeats)
        self.AnalyseHand = PokerAnalyseHand(self.Platform, self.TableType, self.NumberOfSeats, self.FlopSize)

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
            result['hand_analisys'] = self.AnalyseHand.analyse_hand(result)
        return result
