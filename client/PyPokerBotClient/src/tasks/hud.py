import os
from time import sleep
from settings import settings
from osinterface.win32.screenshot import capture_screenshot
from osinterface.win32.hwnd_check import is_minimized,is_window_with_focus
from model.PokerBot import PokerBot
from model.PokerTableScanner import PokerTableScanner


def get_time_to_sleep():
    return settings['SLEEP_TIME_BETWEEN_CAPTURE_MS'] / 1000


def execute(args):
    analisys = ''
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                sleep(get_time_to_sleep())
                if is_minimized(current_table.hwnd):
                    continue
                if not is_window_with_focus(current_table.hwnd):
                    continue
                im = capture_screenshot(current_table.hwnd,
                                        os.path.join(settings['SAMPLES_FOLDER'],
                                                     current_table.get_screenshot_name()))
                result = current_table.refresh_from_image(im)
                result = current_table.generate_decision(result)
                if True or current_table.has_command_to_execute(result):
                    final_analisys = ''
                    final_analisys += '====================================\n'
                    if current_table.has_command_to_execute(result):
                        final_analisys += 'Command           :{}\n'.format(result['commands'][result['command']['to_execute'] - 1])
                        final_analisys += 'Decision          :{}\n'.format(result['decision']['decision'])
                    final_analisys += '------------------------------------\n'
                    final_analisys += 'Number of Villains:{}\n'.format(len([x for x in result['cards'] if x]))
                    final_analisys += 'Flop              :{}\n'.format("".join(result['flop']))
                    final_analisys += 'Pocket Cards      :{}\n'.format(result['hero']['hero_cards'])
                    final_analisys += 'Position          :{}\n'.format(result['hero']['position'])
                    if current_table.has_command_to_execute(result):
                        final_analisys += 'Equity            :{}'.format(result['hand_analisys']['result'])
                    if final_analisys == analisys:
                        continue
                    analisys = final_analisys
                    PokerTableScanner.generate_analisys_summary(final_analisys.strip())
                    im.save(os.path.join(settings['SAMPLES_FOLDER'], current_table.get_screenshot_name()))
                    #run_command(current_table.hwnd, res['command']['TO_EXECUTE'], res)

