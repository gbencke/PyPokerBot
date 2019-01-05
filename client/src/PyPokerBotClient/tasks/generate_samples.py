import os
from time import sleep
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import capture_screenshot
from PyPokerBotClient.model.PokerBot import PokerBot


def usage():
    return "Test"


def execute(args):
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                capture_screenshot(current_table.hwnd,
                                   os.path.join(Settings.get_sample_folder(),
                                                current_table.get_screenshot_name()))
        sleep(Settings.get_time_between_sleeps())
