"""
This module contains all the code to send clicks to a PokerClient GUI
"""
import logging
from time import sleep
import win32gui
import pyautogui

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings


def set_raise_to_pot(hwnd, platform, tabletype):
    """
    Sends the command to raise the bet to pot value.

    :param hwnd: The HWND of the poker table.
    :param platform: The Poker platform that we are using as specified on settings.py
    :param tabletype: The Poker Table Type as specified on settings.py
    :return: None
    """
    current_x = (int(Settings.get_pot_pos(platform, tabletype)[0]) + 20) / 1.25
    current_y = (int(Settings.get_pot_pos(platform, tabletype)[1]) + 20) / 1.25
    logging.debug('Click on set raise to pot')
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.click(current_x, current_y)
    sleep(0.2)
    pyautogui.moveTo(20, 20)


def run_command(hwnd, button_to_press, analisys, platform, tabletype):
    """
    Sends a click to a button on a certain Poker Table Client.

    :param hwnd: The HWND of the poker table.
    :param button_to_press: The index of the button to press.
    :param analisys: The dictionary returned from a PokerTableScanner instance
    :param platform: The Poker platform that we are using as specified on settings.py
    :param tabletype: The Poker Table Type as specified on settings.py
    :return: None
    """
    if button_to_press == 0:
        button_to_press = 1
    if button_to_press not in [1, 2, 3]:
        return

    if analisys['decision']['decision'] == 'RAISE' and \
            analisys['decision']['RAISE_STRATEGY'] == 'POT':
        set_raise_to_pot(hwnd, platform, tabletype)

    current_x = (int(Settings.get_command_pos(platform, tabletype, button_to_press)[0]) + 20) / 1.25
    current_y = (int(Settings.get_command_pos(platform, tabletype, button_to_press)[1]) + 20) / 1.25
    logging.debug('Click on button {}, pos ({},{})'.format(button_to_press, current_x, current_y))
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.click(current_x, current_y)
    sleep(0.1)
    pyautogui.moveTo(20, 20)
