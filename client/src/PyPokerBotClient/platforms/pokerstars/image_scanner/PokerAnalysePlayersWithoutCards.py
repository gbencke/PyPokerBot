# coding=utf-8
import cv2

from PyPokerBotClient.platforms.utils import create_list_boolean_with_number_seats
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


class PokerAnalysePlayersWithoutCards:
    def __init__(self, Platform, TableType, NumberOfSeats):
        self.Platform = Platform
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        pass

    def analyse_players_without_cards(self, Image):
        ret = create_list_boolean_with_number_seats(self.NumberOfSeats)
        for index in range(self.NumberOfSeats):
            empty_card_key = Settings.get_player_hasnocard_template(self.Platform, index)
            empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))

            current_pos_key = 'PLAYER{}_HASCARD'.format(index + 1)
            current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
                Image,
                Settings.get_command_current_pos_key(self.Platform, self.TableType, current_pos_key),
                Settings.get_playerhascard_size(self.Platform, self.TableType)))
            res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
            ret[index] = True if res > Settings.get_play_hascard_threshold(self.Platform, self.TableType) else False
        return ret
