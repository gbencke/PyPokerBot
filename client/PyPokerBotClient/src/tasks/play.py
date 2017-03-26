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
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                im = capture_screenshot(current_table.hwnd,
                                        os.path.join(settings['SAMPLES_FOLDER'],
                                                     current_table.get_screenshot_name()))
                res = current_table.refresh_from_image(im)
                res = current_table.generate_decision(res)
                if current_table.has_command_to_execute(res):
                    logging.debug('-------------')
                    logging.debug('Seats       :' + str(res['seats']))
                    logging.debug('Cards       :' + str(res['cards']))
                    logging.debug('Hero        : ' + str(res['hero']))
                    logging.debug('Flop        : ' + str(res['flop']))
                    logging.debug('Button      : ' + str(res['button']))
                    logging.debug('-------------')
                    logging.debug('Commands    : ' + str(res['commands']))
                    logging.debug('-------------')
                    logging.debug('Decision    : ' + str(res['decision']))
                    logging.debug('Command     : ' + str(res['command']))
                    logging.debug('-------------')
                    im.save(os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()))
                    run_command(current_table.hwnd, res['command']['TO_EXECUTE'], res)
        sleep(get_time_to_sleep())
