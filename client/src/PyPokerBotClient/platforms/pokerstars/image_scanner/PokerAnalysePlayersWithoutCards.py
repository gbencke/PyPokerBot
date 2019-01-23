# coding=utf-8
"""
This module contains a class that checks if the positions on the poker table image
are without cards or not. The opposite of the PokerAnalysePlayersWithCards class.
"""
import cv2

from PyPokerBotClient.platforms.utils import create_list_boolean_seats
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.win32.screenshot \
    import grab_image_from_file, grab_image_pos_from_image


class PokerAnalysePlayersWithoutCards(object):
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

    def analyse_players_without_cards(self, image_to_analyse):
        """
        This is the main method of the class, as it scans the seated positions on the
        poker table image and return a list of booleans indicating that this position
        has or not playing cards.

        :param Image: The source image to scan
        :return: A List of booleans indicating if the position doesnt have cards
        """
        ret = create_list_boolean_seats(self.number_of_seats)
        for index in range(self.number_of_seats):
            empty_card_key = Settings.get_player_hasnocard_template(self.platform, index)
            empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))

            current_pos_key = 'PLAYER{}_HASCARD'.format(index + 1)
            current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
                image_to_analyse,
                Settings.get_command_current_pos_key(
                    self.platform,
                    self.table_type,
                    current_pos_key),
                Settings.get_playerhascard_size(self.platform, self.table_type)))
            res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
            ret[index] = \
                True if res > Settings.get_play_hascard_threshold(
                    self.platform,
                    self.table_type) else False
        return ret
