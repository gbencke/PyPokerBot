"""
This module contains a class that analyses the commands available to the Poker Player on the current
Table being played.
"""
# coding=utf-8
import subprocess
import cv2
import datetime
import os
import logging

from time import sleep
from datetime import datetime

from PyPokerBotClient.platforms.utils import get_histogram_from_image
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings


class PokerAnalyseCommands(object):
    """
    This class verifies which commands (Buttons are available to the poker) are in the current image to
    be used by the player. It crops the image, and then uses a OCR program called Tesseract to try to
    convert the image into a string.
    """

    def __init__(self, Platform, TableType, BB):
        """
        The constructor for the class, takes as parameter the Poker Platform to use, the Table Type
        to analyse and the value of the BigBlind

        :param Platform: The Poker Platform as specified on the settings.py file
        :param TableType: The Table Type as specified on the settings.py file
        :param BB: The current Table Big Blind
        """
        self.Platform = Platform
        self.TableType = TableType
        self.BB = BB

    def generate_command_tuple(self, str):
        """
        This method takes as parameter the string returned from Tesseract and then tries
        to parse the string in order to get the correct command and if there is a value
        on the command like: "Raise $0.25", tries to get this value.

        :param str: The string to parse
        :return: A Tuple containing the command string: FOLD, RAISE, CHECK or CALL, a value
             and the original string
        """
        command = ''
        value = ''
        if 'FOLD' in str.upper():
            command = 'FOLD'
        if 'RAISE' in str.upper():
            command = 'RAISE'
        if 'CHECK' in str.upper():
            command = 'CHECK'
        if 'CALL' in str.upper():
            command = 'CALL'
        if '$' in str:
            value = str.split('$')[1].strip()
            value = float(value) / self.BB
        return command, value, str

    def analyse_commands(self, im):
        """
        This is the default method for this class, as it receives the screenshot of the table
        and then analyse the image to check for the current buttons being shown, it uses Tesseract
        to OCR the cropped positions to transform the image into a string.

        :param im: The Table ScreenShot to be parsed
        :return: A List of Tuples, each tuple containing the command found, its value (if
            available) and the original string from Tesseract
        """
        ret = ['', '', '']

        for x in range(3):
            current_command = x + 1

            template_has_command_cv2_hist = \
                get_histogram_from_image(
                    grab_image_from_file(
                        Settings.get_command_test_template(self.Platform, self.TableType, current_command)))

            has_command_cv2_hist = \
                get_histogram_from_image(grab_image_pos_from_image(
                    im,
                    Settings.get_comand_pos(self.Platform, self.TableType, current_command),
                    Settings.get_command_test_size(self.Platform, self.TableType)))

            res = cv2.compareHist(template_has_command_cv2_hist, has_command_cv2_hist, 0)
            if res > Settings.get_command_test_tolerance(self.Platform, self.TableType):
                im_command = grab_image_pos_from_image(
                    im,
                    Settings.get_command_pos(self.Platform, self.TableType, current_command),
                    Settings.get_command_size(self.Platform, self.TableType))
                command_image_name = 'command{}.jpg'.format(current_command)
                im_command.save(command_image_name)
                return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                                shell=True)
                if len(return_from_tesseract.strip()) == 0:
                    error_filename = command_image_name + '.error.' + datetime.now().strftime(
                        "%Y%m%d%H%M%S.%f") + '.jpg'
                    logging.debug("ERROR ON TESSERACT!!! " + error_filename)
                    im_command.save(error_filename)
                ret[x] = self.generate_command_tuple(return_from_tesseract.replace('\r\n', ' ').replace('  ', ' '))
                os.remove(command_image_name)
                sleep(0.2)
            else:
                ret[x] = ('', 0, '')
        return ret
