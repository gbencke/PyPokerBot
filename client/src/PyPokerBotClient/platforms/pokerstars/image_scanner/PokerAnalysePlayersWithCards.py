# coding=utf-8
import cv2
from PyPokerBotClient.platforms.utils import create_list_boolean_with_number_seats
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


class PokerAnalysePlayersWithCards:
    def __init__(self, Platform, TableType, NumberOfSeats):
        self.Platform = Platform
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.player_has_card_histogram = None
        self.player_has_card_threshold = None

    def analyse(self):
        pass

    def get_player_has_card_threshold(self):
        if self.player_has_card_threshold is None:
            self.player_has_card_threshold = Settings.get_play_hascard_threshold(self.Platform, self.TableType)
        return self.player_has_card_threshold

    def get_player_hascard_histogram(self):
        if self.player_has_card_histogram is None:
            self.player_has_card_histogram = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_player_has_unknown_card_template(self.Platform)))
        return self.player_has_card_histogram

    def get_player_has_card_in_position_histogram(self, index, Image):
        return \
            get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    Settings.get_player_hascard(self.Platform, self.TableType, index),
                    Settings.get_playerhascard_size(self.Platform, self.TableType)))

    def analyse_players_with_cards(self, Image):
        ret = create_list_boolean_with_number_seats(self.NumberOfSeats)
        for current_seat_index in range(self.NumberOfSeats):
            res = cv2.compareHist(
                self.get_player_hascard_histogram(),
                self.get_player_has_card_in_position_histogram(current_seat_index, Image), 0)
            ret[current_seat_index] = True if res > self.get_player_has_card_threshold() else False
        return ret
