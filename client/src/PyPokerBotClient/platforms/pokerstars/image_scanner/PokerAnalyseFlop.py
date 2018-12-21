# coding=utf-8
import numpy
import cv2
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute
from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.platforms.utils import create_list_none_with_number_seats
from PyPokerBotClient.platforms.utils import get_suite_from_image
from PyPokerBotClient.platforms.utils import get_card_template
from PyPokerBotClient.platforms.utils import create_list_string_with_number_seats
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


class PokerAnalyseFlop:

    def __init__(self, Platform, TableType, NumberOfSeats, FlopSize):
        self.Platform = Platform
        self.FlopSize = FlopSize
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.button_template_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.flop_has_card_histogram = create_list_none_with_number_seats(self.NumberOfSeats)
        self.flop_has_card_threshold = None

    def get_flop_hascard_histogram(self, index):
        if self.flop_has_card_histogram[index] is None:
            self.flop_has_card_histogram[index] = get_histogram_from_image(
                grab_image_from_file(
                    Settings.get_flop_has_nocard_template(self.Platform, self.TableType)))
        return self.flop_has_card_histogram[index]

    def get_flop_has_card_threshold(self):
        if self.flop_has_card_threshold is None:
            self.flop_has_card_threshold = \
                Settings.get_play_hascard_threshold(self.Platform, self.TableType)
        return self.flop_has_card_threshold

    def check_if_flop_pos_is_empty(self, Image, index):
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
        flop_card_key = 'FLOPCARD{}'.format(index + 1)
        image_from_flop_card = grab_image_pos_from_image(
            Image,
            Settings.get_flop_card_key(self.Platform, self.TableType, flop_card_key),
            Settings.get_flopcard_size(self.Platform, self.TableType))
        return image_from_flop_card, numpy.array(image_from_flop_card)[:, :, ::-1].copy()

    def analyse_flop_template(self, Image):
        ret = create_list_string_with_number_seats(self.NumberOfSeats)
        for index in range(self.FlopSize):
            if self.check_if_flop_pos_is_empty(Image, index):
                return ret
            selected_card = ''
            selected_card_res = 1000000000
            image_from_flop_card, current_flop_image = self.get_card_in_flop_pos_is_empty(Image, index)
            for current_suit in PokerTableScanner.suits:
                for current_card in PokerTableScanner.cards:
                    template_image, current_card_image = get_card_template(self.Platform, current_card, current_suit)
                    res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                    if res < selected_card_res:
                        selected_card = current_card + current_suit
                        selected_card_res = res
            correct_suit = get_suite_from_image(image_from_flop_card)
            if correct_suit != selected_card[1]:
                selected_card = selected_card[0] + correct_suit
            ret[index] = selected_card
        return ret
