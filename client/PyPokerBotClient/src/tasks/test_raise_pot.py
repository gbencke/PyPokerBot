import logging
import os
import time
import logging
from settings import settings
from helpers.win32.hwnd import scan_windows, set_raise_to_pot
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
    for current_table in pokerstars_tables:
        im = capture_screenshot(current_table.hwnd,
                                os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()), False)
        set_raise_to_pot(current_table.hwnd)
