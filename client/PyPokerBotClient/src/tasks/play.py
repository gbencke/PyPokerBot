import logging
import os
import time
from settings import settings
from analyse_table import generate_analisys,has_command_to_execute
from helpers.win32.hwnd import scan_windows, run_command
from helpers.win32.screenshot import capture_screenshot
from platforms.pokerstarts.detection import is_pokerstars_lobby, is_pokerstars_table
from platforms.pokerstarts.helpers import get_table_name, get_table_stakes, get_table_format
from model.PokerLobby import PokerLobby
from model.PokerTable import PokerTable




def execute(args):
    windows_found = scan_windows()
    pokerstars_lobby_hwnd = [x for x in windows_found if is_pokerstars_lobby(x['class'], x['title'])]
    pokerstars_tables_hwnd = [x for x in windows_found if is_pokerstars_table(x['class'], x['title'])]
    logging.debug(pokerstars_lobby_hwnd)
    logging.debug(pokerstars_tables_hwnd)

    pokerstars_lobby = [PokerLobby(hwnd=x['hwnd'], lobby_name=x['title']) for x in pokerstars_lobby_hwnd]
    pokerstars_tables = [PokerTable(hwnd=x['hwnd'],
                                    name=get_table_name(x['title']),
                                    stakes=get_table_stakes(x['title']),
                                    format=get_table_format(x['title'])) for x in pokerstars_tables_hwnd]
    while True and len(pokerstars_tables) > 0:
        for current_table in pokerstars_tables:
            im = capture_screenshot(current_table.hwnd,
                               os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()), False)
            res = generate_analisys(im)
            if has_command_to_execute(res):
                logging.debug('-------------')
                logging.debug('Seats       :' + str(res['seats']))
                logging.debug('Cards       :' + str(res['cards']))
                logging.debug('Hero        : ' + str(res['hero']))
                logging.debug('Flop        : ' + str(res['flop']))
                logging.debug('Button      : ' + str(res['button']))
                logging.debug('-------------')
                #logging.debug('HandAnalisys: ' + str(res['hand_analisys']))
                logging.debug('Commands    : ' + str(res['commands']))
                logging.debug('-------------')
                logging.debug('Decision    : ' + str(res['decision']))
                logging.debug('Command     : ' + str(res['command']))
                logging.debug('-------------')
                im.save(os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()))
                run_command(current_table.hwnd, res['command']['TO_EXECUTE'], res)

            time.sleep(settings['SLEEP_TIME_BETWEEN_CAPTURE_MS'] / 1000)

