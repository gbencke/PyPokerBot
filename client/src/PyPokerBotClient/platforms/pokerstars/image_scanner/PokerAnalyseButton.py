# coding=utf-8
"""
This module contains the class that analyses the button position on the
screenshot of a PokerStars Playing Table
"""
import cv2

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.platforms.utils import create_list_seats
from PyPokerBotClient.platforms.utils import create_list_boolean_seats
from PyPokerBotClient.osinterface.win32.screenshot \
    import grab_image_from_file, grab_image_pos_from_image


class PokerAnalyseButton(object):
    """
    The button is a marker that indicates that a certain player will the last
    to play on a poker hand, this is very important as he has seen how all other
    players have played before him and this might be a great advantage.

    This class analisys a image and then checks for each seated position if
    it has the button or not, and using the method *analyse_button* returns a
    list of booleans indicating if it has the button or not.
    """

    def __init__(self, platform, table_type, number_of_seats):
        """
        Class Constructor that takes as parameter, the Poker Platform being used,
        the TableType and the Number of Seats, important to notice that all of these
        constants need to be specified on the settings.py file

        :param Platform: The Poker Platform as specified on the settings.py file
        :param TableType: The TableType as specified on the settings.py file
        :param NumberOfSeats: A Integer specifying the Number of Seats for this table
        """
        self.platform = platform
        self.table_type = table_type
        self.number_of_seats = number_of_seats
        self.button_template_histogram = create_list_seats(self.number_of_seats)

    def get_player_hasbutton_histogram(self, index):
        """
        Returns a histogram (A OpenCV data structure representing the color
        structure on a image), for a specific hasbutton template for a specific seat on the table.

        :param index: The index of the seat on the poker table
        :return: The OpenCV Histogram
        """
        if self.button_template_histogram[index] is None:
            self.button_template_histogram[index] = get_histogram_from_image(
                grab_image_from_file(Settings.get_button_template_file(self.platform, index)))
        return self.button_template_histogram[index]

    def analyse_button(self, image_to_analyse):
        """
        This is the main method for the class, that takes a image as parameter and
        then check for each seated position if the button marker is in the position

        :param Image: The screenshot of the Poker Table to analyse
        :return: A List of booleans for each seated position indicating if the position
             has the button or not.
        """
        ret = create_list_boolean_seats(self.number_of_seats)
        for index in range(self.number_of_seats):
            current_seat_cv2_hist = get_histogram_from_image(
                grab_image_pos_from_image(
                    image_to_analyse,
                    Settings.get_button_template(self.platform, self.table_type, index),
                    Settings.get_button_size(self.platform, self.table_type)))
            res = cv2.compareHist(
                self.get_player_hasbutton_histogram(index),
                current_seat_cv2_hist, 0)
            button_threshold = Settings.get_button_threshold(
                self.platform,
                self.table_type)
            ret[index] = True if res > button_threshold else False
        return ret
