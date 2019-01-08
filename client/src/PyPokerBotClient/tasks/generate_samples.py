"""
This Task generates a series of screenshots from the Poker desktop client that is
running on the computer. It saves them as JPEG images for later analisys. Those
samples are saved on the samples_folder key of the settings.py configuration file

Usage:
::

    python PyPokerBot.py generate_samples


Parameters:

    **None**

Return:

    **None**

Obs:

    The samples are saved on the folder specified on the samples_folder key of the
    dictionary returned by settings.py

"""

import os
from time import sleep
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import capture_screenshot
from PyPokerBotClient.model.PokerBot import PokerBot


def usage():
    """Display the current task (generate_samples) usage

    :return:  None (Prints the usage information to stdout)
    """
    return \
        """
        This Task generates a series of screenshots from the Poker desktop client that is
        running on the computer. It saves them as JPEG images for later analisys. Those
        samples are saved on the samples_folder key of the settings.py configuration file

        Usage:
        ::

            python PyPokerBot.py generate_samples


        Parameters:

            **None**

        Return:

            **None**

        Obs:

            The samples are saved on the folder specified on the samples_folder key of the
            dictionary returned by settings.py
        """


def execute(args):
    """Execute is the main entry point for this task module. It starts the loop that generate the
    samples from capturing the poker client desktop image.

    :param args: None

    :return: None (Saves the samples to the sample_folder specified in settings.py)
    """
    while True:
        lobbies = PokerBot.scan_for_lobbies()
        for current_lobby in lobbies:
            for current_table in current_lobby.get_tables():
                capture_screenshot(current_table.hwnd,
                                   os.path.join(Settings.get_sample_folder(),
                                                current_table.get_screenshot_name()))
        sleep(Settings.get_time_between_sleeps())
