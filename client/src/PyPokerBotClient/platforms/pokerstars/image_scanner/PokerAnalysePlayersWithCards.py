# coding=utf-8
"""
This module contains the class that analyses if a seated position on the table contains
playing cards or not (it is participating on the hand).
"""
import cv2

from PyPokerBotClient.platforms.utils import create_list_boolean_seats
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.image import \
    grab_image_from_file, grab_image_pos_from_image


class PokerAnalysePlayersWithCards(object):
    """
    This class analyses which seated positions on a poker table image are playing on
    a certain hand. The main method returns a list of Booleans indicating which position is
    playing or not.
    """

    def __init__(self, platform, table_type, number_of_seats):
        """
        This is the constructor for this class, it takes as parameter the
        Poker Platform to be used, the TableType, the number of available seats
        and the maximum number of cards on the flop.

        :param Platform: The Poker Platform, in our case, it must be POKERSTARS
        :param TableType: The Table Type as in the settings.py file like: 6-SEATS
        :param NumberOfSeats: A integer representing the number of seats on the table
        """
        self.platform = platform
        self.table_type = table_type
        self.number_of_seats = number_of_seats
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None

    def get_player_has_card_threshold(self):
        """
        This method returns a number value indicating the threshold (confidence level) for
        histogram comparison between the actual image of the position and a template that indicate
        that the player has cards

        :return: Threshold value from settings.py
        """
        if self.player_has_card_threshold is None:
            self.player_has_card_threshold = \
                Settings.get_play_hascard_threshold(self.platform, self.table_type)
        return self.player_has_card_threshold

    def get_player_hascard_histogram(self):
        """
        This method returns the histogram for the template image (defined on settings.py that
        we will use to compare with the current image in order to check if the position
        contains cards or not.

        :return: The Histogram of the Template Image from settings.py
        """
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_has_unknown_card_template(self.platform)))
        return self.player_has_card_histogram

    def get_has_card_in_pos_histogram(self, index, image_to_analyse):
        """
        This method returns the histogram of the image of the cards on a certain position
        of the table. This image will be compared with the template specified on the
        settings.py file and if it is above the threshold specified on settings.py, that
        position will be determined that there are cards

        :param index: The index of the position on the table to analyse
        :param Image: The source image
        :return: The Histogram data structure to be used for comparison
        """
        return \
            get_histogram_from_image(
                grab_image_pos_from_image(
                    image_to_analyse,
                    Settings.get_player_hascard(self.platform, self.table_type, index),
                    Settings.get_playerhascard_size(self.platform, self.table_type)))

    def analyse_players_with_cards(self, image_to_analyse):
        """
        This is the main method of the class, as it scans the seated positions on the
        poker table image and return a list of booleans indicating that this position
        has or not playing cards.

        :param Image: The source image to scan
        :return: A List of booleans indicating if the position has cards or not.
        """
        ret = create_list_boolean_seats(self.number_of_seats)
        for current_seat_index in range(self.number_of_seats):
            res = cv2.compareHist(
                self.get_player_hascard_histogram(),
                self.get_has_card_in_pos_histogram(
                    current_seat_index,
                    image_to_analyse), 0)
            ret[current_seat_index] = \
                True if res > self.get_player_has_card_threshold() else False
        return ret
