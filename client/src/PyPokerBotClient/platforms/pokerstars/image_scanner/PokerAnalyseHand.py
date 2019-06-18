# coding=utf-8
"""
This module contains the class that analisys from a screenshot of a poker table, the current
player hand and its strength.
"""
import ast
import requests

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.platforms.utils import create_list_seats


class PokerAnalyseHand(object):
    """
    This class analyses from a poker table screenshot, the current cards of the player and
    their strength. It takes as input a dictionary returned from the other classes of these
    package
    """

    def __init__(self, platform, table_type, number_of_seats, flop_size):
        """
        This is the constructor for this class, it takes as parameter the
        Poker Platform to be used, the TableType, the number of available seats and
        the maximum number of cards on the flop.

        :param Platform: The Poker Platform, in our case, it must be POKERSTARS
        :param TableType: The Table Type as in the settings.py file like: 6-SEATS
        :param NumberOfSeats: A integer representing the number of seats on the table
        :param FlopSize: The maximum number of cards on the flop
        """
        self.platform = platform
        self.table_type = table_type
        self.number_of_seats = number_of_seats
        self.flop_size = flop_size
        self.button_template_histogram = create_list_seats(self.number_of_seats)

    def get_flop_cards(self, analisys):
        """
        This utility method returns a single concatenated string from the list of cards on
        the flop according to the analisys dictionary that was created by the other classes
        on this package.

        :param analisys: A analisys dictionary created by analyse from image method of the
             PokerTableScannerPokerStars class
        :return: A string containing all the cards concatenated

        """
        return "".join([analisys['flop'][x] for x in range(self.flop_size)])

    def analyse_hand_phase(self, analisys):
        """
        This utility determines the phase of the hand according to the number of cards
        on the flop as indicated on the analisys dictionary. The phases are:
        PREFLOP, FLOP, RIVER, TURN

        :param analisys: A analisys dictionary created by analyse from image method of the
             PokerTableScannerPokerStars class
        :return: A string containing the current hand phase
        """
        number_cards_on_flop = len(self.get_flop_cards(analisys)) / 2
        if number_cards_on_flop == 0:
            return 'PREFLOP'
        else:
            return 'FLOP{}'.format(number_cards_on_flop)

    def analyse_hand(self, analisys):
        """
        This is the main method of the class, as it takes as parameter the dictionary created
        by the other classes of these package in the PokerTableScannerPokerStars analyse from image
        method.

        :param analisys: A analisys dictionary created by analyse from image method of the
             PokerTableScannerPokerStars class
        :return: The Current strength of the hand as returned by the PokerBotServer
        """
        ret = {}
        if len(analisys['hero']['hero_cards']) == 0:
            return ret
        flop_cards = self.get_flop_cards(analisys)
        ret['hand_phase'] = self.analyse_hand_phase(analisys)
        if ret['hand_phase'] == 'PREFLOP':
            pocket_cards_to_server = analisys['hero']['hero_cards'] + ":XX"
        else:
            total_villains = len([x for x in analisys['cards'] if x])
            # We don't have performance for more than 2 villains so...
            total_villains = 2 if total_villains > 2 else total_villains
            pocket_cards_to_server = analisys['hero']['hero_cards'] + \
                                     ":" + ":".join(['XX'] * total_villains)

        _, result = self.send_hands_to_server(pocket_cards_to_server, flop_cards)
        ret['result'] = result
        return ret

    @staticmethod
    def send_hands_to_server(pocket_cards, flop_cards):
        """
        This method sends a URL request to the pokerbot server in
        order to calculate the equity of the current hand, this equity
        is the probability that the current cards will be the winning hand

        :param pocket_cards: The cards that the player holds
        :param flop_cards: The command cards on the flop
        :return: A Number indicating the percentage that this will be the winning hand...
        """
        command_to_send = '{} {}'.format(pocket_cards, flop_cards)
        request_made = requests.post(
            Settings.get_calculate_url(),
            json={"command": command_to_send})
        returned_equity = request_made.content.decode('UTF-8')
        if request_made.status_code == 200 and returned_equity != 'Error':
            return command_to_send, ast.literal_eval(returned_equity)
        else:
            return command_to_send, ''
