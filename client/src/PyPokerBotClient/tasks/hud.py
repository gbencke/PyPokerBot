import os
import logging
import traceback
from time import sleep
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import capture_screenshot
from PyPokerBotClient.osinterface.win32.hwnd_check import is_minimized, is_window_with_focus
from PyPokerBotClient.model.PokerBot import PokerBot
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute


def get_time_to_sleep():
    return Settings.get_time_between_sleeps() / 1000


def execute(args):
    logging.info("Starting HUD....")
    if len(args) > 0:
        total_secs = int(args[0])
        logging.info("Will sleep for {}....".format(args[0]))
        for x in range(total_secs):
            logging.info("Sleeping({})".format(total_secs - x))
            sleep(1)
    analisys = ''
    while True:
        try:
            sleep(get_time_to_sleep())
            lobbies = PokerBot.scan_for_lobbies()
            for current_lobby in lobbies:
                for current_table in current_lobby.get_tables():
                    if is_minimized(current_table.hwnd):
                        continue
                    if not is_window_with_focus(current_table.hwnd):
                        continue
                    im = capture_screenshot(current_table.hwnd,
                                            os.path.join(Settings.get_sample_folder(),
                                                         current_table.get_screenshot_name()), should_save=False)
                    result = current_table.refresh_from_image(im)
                    result = current_table.generate_decision(result)
                    if has_command_to_execute(result):
                        final_analisys = '\n'
                        final_analisys += '==========================================================\n'
                        final_analisys += '==========================================================\n'
                        final_analisys += 'Decision          :{}({})\n'.format(
                            result['decision']['decision'],
                            result['decision']['raise_strategy'])
                        final_analisys += 'Equity            :{}%\n'.format(result['hand_analisys']['result'])
                        final_analisys += '----------------------------------------------------------\n'
                        final_analisys += 'Number of Villains:{}\n'.format(len([x for x in result['cards'] if x]))
                        final_analisys += 'Flop              :{}\n'.format("".join(result['flop']))
                        final_analisys += 'Pocket Cards      :{}\n'.format(result['hero']['hero_cards'])
                        final_analisys += 'Position          :{}\n'.format(result['hero']['position'])
                        if final_analisys == analisys:
                            continue
                        analisys = final_analisys
                        PokerTableScanner.generate_analisys_summary_info(final_analisys.strip())
                        im.save(os.path.join(Settings.get_sample_folder(), current_table.get_screenshot_name()))
            if len(lobbies) == 0:
                logging.error('No Lobbies, exiting...')
                exit(0)
            else:
                if len(lobbies[0].get_tables()) == 0:
                    logging.error('No Tables, sleeping 1 sec')
                    sleep(1)
                    continue
        except Exception as e:
            tb = traceback.format_exc()
            logging.error('error:' + str(tb))
