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
from PyPokerBotClient.settings import GlobalSettings as Settings


class PokerAnalyseCommands:

    def __init__(self, Platform, TableType):
        self.Platform = Platform
        self.TableType = TableType
        pass

    def generate_command_tuple(self, str):
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
        return (command, value, str)

    def analyse_commands(self, im):
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
