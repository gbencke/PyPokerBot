# coding=utf-8
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
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.platforms.utils import get_suite_from_image
from PyPokerBotClient.platforms.utils import get_card_template
from PyPokerBotClient.platforms.utils import create_list_string_with_number_seats
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


class PokerAnalyseHero:

    def __init__(self, Platform, TableType, NumberOfSeats):
        self.Platform = Platform
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)

    def get_absolute_hero_pos(self, hero_pos, button):
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
                return self.get_absolute_hero_pos(hero_pos, button)
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
                            template_image, current_card_image = get_card_template(self.Platform, current_card,
                                                                                   current_suit)
                            res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                            if res < selected_card_res:
                                selected_card = current_card + current_suit
                                selected_card_res = res
                    correct_suit = get_suite_from_image(image_from_player)
                    if correct_suit != selected_card[1]:
                        selected_card = selected_card[0] + correct_suit
                    ret['hero_cards'] += selected_card
                break
        hero_position = ''
        if 'hero_pos' in ret:
            hero_position = self.get_hero_position(ret['hero_pos'], cards, button)
        ret['position'] = hero_position
        return ret
