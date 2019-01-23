# coding=utf-8
"""
This module contains the class that analysis the current player (Hero) status on a screenshot
of a poker table, it is used by the PokerTableScannerPokerStars as part of the process of
analysing a certain poker table image.
"""
import numpy
import cv2

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner
from PyPokerBotClient.platforms.utils import get_suite_from_image
from PyPokerBotClient.platforms.utils import get_card_template
from PyPokerBotClient.platforms.utils import create_list_seats
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_pos_from_image


class PokerAnalyseHero(object):
    """
    This class analyses the Hero on a poker table image and then returns a dictionary
    containing both its pocket cards and its position on the table, on the following format:

    Dictionary containing:

    * **position**: Returns the position of the hero on the table as: BUTTON,LP,MP,BB,or SB
    * **hero_pos**: Returns the position of the hero on the table as a integer
    * **hero_cards**: Returns the pocket cards of the hero

    Example:
    ::

    {'position': 'BB', 'hero_pos': 3, 'hero_cards': '5sKh'}

    """

    def __init__(self, platform, table_type, number_of_seats):
        """
        This is the constructor for this class, it takes as parameter the Poker
        Platform to be used, the TableType, the number of available seats and the
        maximum number of cards on the flop.

        :param Platform: The Poker Platform, in our case, it must be POKERSTARS
        :param TableType: The Table Type as in the settings.py file like: 6-SEATS
        :param NumberOfSeats: A integer representing the number of seats on the table
        """
        self.platform = platform
        self.table_type = table_type
        self.number_of_seats = number_of_seats
        self.button_template_histogram = create_list_seats(self.number_of_seats)

    def get_absolute_hero_pos(self, hero_pos, button):
        """
        This function returns the position of the hero on the table based on the distance
        between the hero and the button, the possible values are:

        * **BUTTON**: The Player is on the button
        * **LP**: The Player is in a late position
        * **MP**: The Player is in a middle position
        * **BB**: The Player seats on the big blind
        * **SB**: The Player seats on the small blind

        :param hero_pos: The Hero position as a index of the table seats
        :param button: The index of the table position where the button is.
        :return: One of the strings explained above.
        """
        if len([x for x in button if x]) == 0:
            return 'MP'
        distance = 0
        current_pos_analysed = hero_pos
        while True:
            distance += 1
            if current_pos_analysed == self.number_of_seats:
                current_pos_analysed = 0
            if button[current_pos_analysed]:
                break
            current_pos_analysed += 1
        ret = ''
        if distance == 0:
            ret = 'BUTTON'
        if distance == 1:
            ret = 'LP'
        if distance == 2:
            ret = 'MP'
        if distance == 3:
            ret = 'MP'
        if distance == 4:
            ret = 'BB'
        if distance == 5:
            ret = 'SB'
        return ret

    def get_hero_position(self, hero_pos, cards, button):
        """
        This function returns the position of the hero on the table based on the distance
        between the hero and the button, and based on who is participating on the current
        hand. The possible values are:

        * **BUTTON**: The Player is on the button
        * **LP**: The Player is in a late position
        * **MP**: The Player is in a middle position
        * **BB**: The Player seats on the big blind
        * **SB**: The Player seats on the small blind

        :param hero_pos: The Hero position as a index of the table seats
        :param cards: A list of booleans containg a True/False if the seat has cards or not
        :param button: The index of the table position where the button is.
        :return: One of the strings explained above.
        """
        loop_total = 0
        if button[hero_pos - 1]:
            return 'BUTTON'
        current_pos_analysed = hero_pos
        while True:
            loop_total += 1
            if current_pos_analysed == self.number_of_seats:
                current_pos_analysed = 0
            if cards[current_pos_analysed] or loop_total > 3:
                return self.get_absolute_hero_pos(hero_pos, button)
            if button[current_pos_analysed]:
                return 'BUTTON'
            current_pos_analysed += 1

    def get_hero_card_image(self, image_to_analyse, seat, current_hero_card):
        """
        This method receives as input the Image of the poker table and then
        selects a region of the image, and analisys which card (Value and Suit) is
        represented on that image.

        :param Image: A screenshot of the poker table
        :param seat: The index of the seat on the table
        :param current_hero_card: Position of the Card on the Pocket Cards Set (0 or 1)
        :return: A Image as a numpy array, containing a Card to be analysed.
        """
        flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
        image_from_player = grab_image_pos_from_image(
            image_to_analyse,
            Settings.get_flop_card_key(self.platform, self.table_type, flop_card_key),
            Settings.get_flopcard_size(self.platform, self.table_type))
        current_flop_image = numpy.array(image_from_player)[:, :, ::-1].copy()
        return image_from_player, current_flop_image

    def analyse_hero(self, image_to_analyse, cards, nocards, button):
        """
        This is the main method of the class, it returns a dictionary with the status
        of the Current Player (Hero) on the Poker Table image passed as parameter.

        :param im: The image to analyse.
        :param cards: A List of booleans to indicate which seat has cards or not
        :param nocards: A List of booleans to indicate which seat has cards or not
        :param button: The position of the button as a index to the table seats
        :return: Dictionary containing:

        * **position**: Returns the position of the hero on the table as: BUTTON,LP,MP,BB,or SB
        * **hero_pos**: Returns the position of the hero on the table as a integer
        * **hero_cards**: Returns the pocket cards of the hero

        Example:
        ::

        {'position': 'BB', 'hero_pos': 3, 'hero_cards': '5sKh'}

        """
        ret = {'hero_cards': '', 'position': ''}
        for seat in range(self.number_of_seats):
            if (not cards[seat]) and not nocards[seat]:
                ret['hero_pos'] = seat + 1
                for current_hero_card in range(2):
                    selected_card = ''
                    selected_card_res = 1000000000
                    image_from_player, current_flop_image = \
                        self.get_hero_card_image(image_to_analyse, seat, current_hero_card)
                    for current_suit in PokerTableScanner.suits:
                        for current_card in PokerTableScanner.cards:
                            current_card_image = get_card_template(self.platform, current_card,
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
