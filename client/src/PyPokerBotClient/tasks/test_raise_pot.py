import os
import logging
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.send_clicks import set_raise_to_pot
from PyPokerBotClient.osinterface.win32.screenshot import capture_screenshot
from PyPokerBotClient.model.PokerBot import PokerBot


def usage():
    return "Test"


def execute(args):
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
                        set_raise_to_pot(current_table.hwnd, current_lobby.platform, '6-SEATS')
