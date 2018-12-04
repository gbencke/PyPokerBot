import os
import logging
from time import sleep
from settings import settings
from osinterface.win32.screenshot import capture_screenshot
from model.PokerBot import PokerBot
from osinterface.win32.send_clicks import run_command


def get_time_to_sleep():
    return settings['SLEEP_TIME_BETWEEN_CAPTURE_MS'] / 1000


def execute(args):
    logging.debug("Starting the Play Task...")
    res_last = {}
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                im = capture_screenshot(current_table.hwnd,
                                        os.path.join(settings['SAMPLES_FOLDER'],
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
                        im.save(os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()))
                        run_command(current_table.hwnd, res['command']['to_execute'], res)
                res_last = res
            sleep(get_time_to_sleep())
