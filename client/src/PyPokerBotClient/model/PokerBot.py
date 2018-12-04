import importlib
from custom_exceptions.MoreThanOneLobbyPerPlatformException import MoreThanOneLobbyPerPlatformException
from settings import settings
from osinterface.win32.scan_hwnd import scan_windows


class PokerBot:
    def __init__(self):
        pass

    @staticmethod
    def get_supported_platforms():
        return [settings['PLATFORMS'][x] for x in settings['PLATFORMS']]

    @staticmethod
    def get_instance(classname):
        return getattr(importlib.import_module(classname), classname.split('.')[-1])

    @staticmethod
    def scan_for_lobbies():
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
