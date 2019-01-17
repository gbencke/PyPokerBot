# coding=utf-8
"""
This module contains the class that analyses the flop of the table, which are common cards that all
players can combine with their pocket cards in order to make the best possible hand
"""
import numpy
import cv2

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.platforms.utils import get_suite_from_image
from PyPokerBotClient.platforms.utils import get_card_template
from PyPokerBotClient.platforms.utils import create_list_string_with_number_seats
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


class PokerAnalyseFlop(object):
    """
    This class analyses the flop, which contains the common cards that are shared by all players in order
    to create the best hand. The flop is available on the center of the table, and every turn a card is
    revealed on the flop, so that the players can make decisions
    """

    def __init__(self, Platform, TableType, NumberOfSeats, FlopSize):
        """
        This is the constructor for this class, it takes as parameter the Poker Platform to be used, the
        TableType, the number of available seats and the maximum number of cards on the flop.

        :param Platform: The Poker Platform, in our case, it must be POKERSTARS
        :param TableType: The Table Type as in the settings.py file like: 6-SEATS
        :param NumberOfSeats: A integer representing the number of seats on the table
        :param FlopSize: The maximum number of cards on the flop
        """
        self.Platform = Platform
        self.FlopSize = FlopSize
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.flop_has_card_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.flop_has_card_threshold = None

    def get_flop_hascard_histogram(self, index):
        """
        This function returns the Histogram (OpenCV data structure representing the
        color distribution of a image), that checks if a position on the flop contains a
        card or not

        :param index: The seated position on the table
        :return: A histogram of that position
        """
        if self.flop_has_card_histogram[index] is None:
            self.flop_has_card_histogram[index] = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_flop_has_nocard_template(self.Platform, self.TableType)))
        return self.flop_has_card_histogram[index]

    def get_flop_has_card_threshold(self):
        """
        Returns the "Threshold", the confidence level in regard to the histogram comparison
        to determine if a certain position on the flop contains a card or not.

        :return: A Number representing the required confidence level for comparison
        """
        if self.flop_has_card_threshold is None:
            self.flop_has_card_threshold = \
                Settings.get_play_hascard_threshold(self.Platform, self.TableType)
        return self.flop_has_card_threshold

    def check_if_flop_pos_is_empty(self, Image, index):
        """
        This method checks if a certain position on the flop contains a card or not.

        :param Image: The image of the table being analysed
        :param index: The index of the card on the flop
        :return: True if the position has a Card or False if not.
        """
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
        """
        This method gets the image from a certain position on the table flop

        :param Image: The source image to be cropped
        :param index: The index of the card on the flop
        :return: The image of the specified position as a numpy array
        """
        flop_card_key = 'FLOPCARD{}'.format(index + 1)
        image_from_flop_card = grab_image_pos_from_image(
            Image,
            Settings.get_flop_card_key(self.Platform, self.TableType, flop_card_key),
            Settings.get_flopcard_size(self.Platform, self.TableType))
        return image_from_flop_card, numpy.array(image_from_flop_card)[:, :, ::-1].copy()

    def analyse_flop_template(self, Image):
        """
        This is the main method of the class, as if loops for all the possible positions on
        the flop and then checks if there is a card there, if there is, then by comparision
        see which card is on that flop position, returning a card for each flop position

        :param Image: The source image of the table
        :return: A list of strings containing the cards on the flop.
        """
        ret = create_list_string_with_number_seats(self.NumberOfSeats)
        for index in range(self.FlopSize):
            if self.check_if_flop_pos_is_empty(Image, index):
                return ret
            selected_card = ''
            selected_card_res = 1000000000
            image_from_flop_card, current_flop_image = self.get_card_in_flop_pos_is_empty(Image, index)
            for current_suit in PokerTableScanner.suits:
                for current_card in PokerTableScanner.cards:
                    current_card_image = get_card_template(self.Platform, current_card, current_suit)
                    res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                    if res < selected_card_res:
                        selected_card = current_card + current_suit
                        selected_card_res = res
            correct_suit = get_suite_from_image(image_from_flop_card)
            if correct_suit != selected_card[1]:
                selected_card = selected_card[0] + correct_suit
            ret[index] = selected_card
        return ret
