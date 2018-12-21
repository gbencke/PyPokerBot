# coding=utf-8
import cv2

from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.platforms.utils import create_list_boolean_with_number_seats
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image

class PokerAnalyseButton:

    def __init__(self, Platform, TableType, NumberOfSeats):
        self.Platform = Platform
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)

    def get_player_hasbutton_histogram(self, index):
        if self.button_template_histogram[index] is None:
            self.button_template_histogram[index] = get_histogram_from_image(
                grab_image_from_file(Settings.get_button_template_file(self.Platform, self.TableType, index)))
        return self.button_template_histogram[index]

    def analyse_button(self, Image):
        ret = create_list_boolean_with_number_seats(self.NumberOfSeats)
        for index in range(self.NumberOfSeats):
            current_seat_cv2_hist = get_histogram_from_image(
                grab_image_pos_from_image(
                    Image,
                    Settings.get_button_template(self.Platform, self.TableType, index),
                    Settings.get_button_size(self.Platform, self.TableType)))
            res = cv2.compareHist(self.get_player_hasbutton_histogram(index), current_seat_cv2_hist, 0)
            button_threshold = Settings.get_button_threshold(self.Platform, self.TableType)
            ret[index] = True if res > button_threshold else False
        return ret
