"""
This method contains the main poker bot class that wraps all the business logic of the PokerBot.
"""
import importlib
from PyPokerBotClient.custom_exceptions.MoreThanOneLobbyPerPlatformException import MoreThanOneLobbyPerPlatformException
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.scan_hwnd import scan_windows


class PokerBot(object):
    """
    Main Class for the PyPokerBot, it is responsible for scanning and creating the available
    poker lobbies on the desktop computer where it is running
    """

    def __init__(self):
        """
        Default Constructor
        """
        pass

    @staticmethod
    def get_supported_platforms():
        """
        Returns a list of supported Poker Platforms like 888Poker, PokerStars, Party Poker and others
        :return: A List of strings
        """
        return Settings.get_platforms()

    @staticmethod
    def get_instance(classname):
        """
        Returns a instance of a certain classname in Python format

        :param classname: A string representing a full class name
        :return: A instance of the specified class
        """
        return getattr(importlib.import_module(classname), classname.split('.')[-1])

    @staticmethod
    def scan_for_lobbies():
        """
        This is the main method of the class, as is scan all the windows on the Windows Desktop
        Environment for open poker lobbies that are configured on the settings.py file

        :return: A List of PokerLobby instances
        """
        lobbies_found = []
        windows_found = scan_windows()
        platforms = PokerBot.get_supported_platforms()
        for current_platform in platforms:
            lobby_class = PokerBot.get_instance(current_platform['POKER_LOBBY_CLASS'])
            table_scanner = PokerBot.get_instance(current_platform['POKER_TABLE_SCANNER_CLASS'])
            table_strategy = PokerBot.get_instance(current_platform['POKER_STRATEGY_CLASS'])
            platform_name = current_platform['PLATFORM_NAME']
            lobbies_from_platform_found = lobby_class.scan_for_lobbies(windows_found)
            if len(lobbies_from_platform_found) == 0:
                continue
            if len(lobbies_from_platform_found) > 1:
                raise MoreThanOneLobbyPerPlatformException("Only one lobby allowed for platform".format(platform_name))
            tables_found = lobbies_from_platform_found[0].scan_for_tables(windows_found, table_scanner, table_strategy,
                                                                          lobbies_from_platform_found[0])
            lobbies_from_platform_found[0].add_tables(tables_found)
            lobbies_found += lobbies_from_platform_found
        return lobbies_found
