import os
from time import sleep
from settings import settings
from osinterface.win32.screenshot import capture_screenshot
from model.PokerBot import PokerBot


def execute(args):
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                capture_screenshot(current_table.hwnd,
                                   os.path.join(settings['SAMPLES_FOLDER'],
                                                current_table.get_screenshot_name()))
        sleep(settings['SLEEP_TIME_BETWEEN_CAPTURE_MS'])
