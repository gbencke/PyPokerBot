"""
This tasks stars the PokerBot in Playing mode, so it will capture the screens of the
poker client, parse the image, run the strategy and send the clicks to the poker cliente

Usage:
::

    python PyPokerBot.py play

Parameters:

    **None**

Return:

    **None** (But writes to stdout the parse of the screen image capture)

"""
import os
import logging
from time import sleep
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import capture_screenshot
from PyPokerBotClient.model.PokerBot import PokerBot
from PyPokerBotClient.osinterface.win32.send_clicks import run_command


def usage():
    return \
        """
        This tasks stars the PokerBot in Playing mode, so it will capture the screens of the
        poker client, parse the image, run the strategy and send the clicks to the poker cliente

        Usage:
        ::

            python PyPokerBot.py play

        Parameters:

            **None**

        Return:

            **None** (But writes to stdout the parse of the screen image capture)

        """


def get_time_to_sleep():
    """ Returns the time to sleep between screen captures as defined on settings.py

    :return: Time to sleep between screen captures as defined on settings.py
    """
    return Settings.get_time_between_sleeps() / 1000


def execute(args):
    """
    This tasks stars the PokerBot in Playing mode, so it will capture the screens of the
    poker client, parse the image, run the strategy and send the clicks to the poker cliente

    :param: None

    :return: None (But writes to stdout the parse of the screen image capture)

    """
    logging.debug("Starting the Play Task...")
    res_last = {}
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                im = capture_screenshot(current_table.hwnd,
                                        os.path.join(Settings.get_sample_folder(),
                                                     current_table.get_screenshot_name()))
                res = current_table.refresh_from_image(im)
                res = current_table.generate_decision(res)

                if str(res) != str(res_last):
                    logging.debug('--------------')
                    logging.debug('Seats       : {}'.format(str(res['seats'])))
                    logging.debug('Cards       : {}'.format(str(res['cards'])))
                    logging.debug('Flop        : {}'.format(str(res['flop'])))
                    logging.debug('Button      : {}'.format(str(res['button'])))
                    if 'hero' in res:
                        logging.debug('Hero        : {}'.format(str(res['hero'])))
                    logging.debug('--------------')
                    if current_table.has_command_to_execute(res):
                        logging.debug('Commands    : {}'.format(str(res['commands'])))
                        logging.debug('--------------')
                        logging.debug('Decision    : {}'.format(str(res['decision'])))
                        logging.debug('Command     : {}'.format(str(res['command'])))
                        im.save(os.path.join(Settings.get_sample_folder(), current_table.get_screenshot_name()))
                        run_command(current_table.hwnd, res['command']['to_execute'], res, current_lobby.platform,
                                    '6-SEATS')
                res_last = res
            sleep(get_time_to_sleep())
