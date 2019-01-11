"""
Every poker platform client software has 2 main components: The Poker Lobby and the Poker Tables.
Normally, there is only one poker lobby for every platform, where the player can check its balance
see the incoming events and also the available tables, and also select a certain table to seat.
"""
from PyPokerBotClient.model.PokerLobby import PokerLobby
from PyPokerBotClient.model.PokerTable import PokerTable


class PokerLobbyPokerStars(PokerLobby):
    """
    The PokerLobbyPokerStars class encapsulates all the functionality that is needed to
    manipulate and interact with the Poker Lobby of the Poker Stars platform,
    the table instances that the PokerBot is going to interact with, are generated from
    the lobby instance, and there is only one poker lobby instance per poker platform (Singleton).

    This class is a specialization of the generic PokerLobby class that shares many
    generic methods with its specialized classes
    """

    def __init__(self, hwnd, lobby_name):
        """
        Main Constructor for the PokerStars Lobby
        :param hwnd: HWND (Window Handle) for the Lobby window
        :param lobby_name: Window Title
        """
        PokerLobby.__init__(self)
        self.hwnd = hwnd
        self.lobby_name = lobby_name
        self.tables = []
        self.platform = 'POKERSTARS'

    @staticmethod
    def scan_for_lobbies(hwnd_to_scan):
        """
        This static method receives a list of windows to check if anyone of them is
        a poker star lobby and return a list of valid lobbies.

        :param hwnd_to_scan:  List of Windows Handles to check (HWND)
        :return: List of lobbies (Actually can there only be ONE Lobby)
        """
        ret = []
        for current_hwnd in hwnd_to_scan:
            if PokerLobbyPokerStars.is_pokerstars_lobby(current_hwnd['class'], current_hwnd['title']):
                ret.append(PokerLobbyPokerStars(current_hwnd['hwnd'], current_hwnd['title']))
        return ret

    @staticmethod
    def is_pokerstars_lobby(classname, window_text):
        """
        Using the Windows classname and also the text of the title of the window,
        we can check if the window is a Poker Stars Lobby.

        :param classname: The windows classname of the window
        :param window_text: The Title of the window
        :return: True of False
        """
        return 'POKERSTARS LOBBY' in window_text.upper()

    @staticmethod
    def is_pokerstars_table(classname, window_text):
        """
        Using the Windows classname and also the text of the title of the window,
        we can check if the window is a Poker Stars Table
        :param classname: The windows classname of the window
        :param window_text: The Title of the window
        :return: True of False
        """
        return 'PokerStarsTableFrameClass'.upper() in classname.upper()

    @staticmethod
    def get_table_name(title):
        """
        Parsing the window title of the table, we can determine the name of the
        poker table

        :param title: The window title
        :return: The Title of the table
        """
        return title.split('-')[0].strip()

    @staticmethod
    def get_table_stakes(title):
        """
        Parsing the window title of the table, we can determine the stakes of
        such table

        :param title: The window title
        :return: The stakes of the table
        """
        return title.split('-')[1].strip()

    @staticmethod
    def get_table_format(title):
        """
        Parsing the window title of the table, we can determine the format of
        such table (HOLDEM, OMAHA, etc...)

        :param title: The window title
        :return: The format of the table
        """
        return title.split('-')[2].strip()

    def add_tables(self, tables_to_add):
        """
        Add a list of tables to the current instance table list.

        :param tables_to_add: List of tables to add
        :return: None
        """
        self.tables += tables_to_add

    def get_tables(self):
        """
        Return the current tables that were found the current lobby

        :return: List of current tables for the lobby
        """
        return self.tables

    def sanitize_string(self, str):
        """
        Perform simple sanitization of the table title (remove any
        unnecessary strings) and return a cleaned string.

        :param str: The window title to sanitize
        :return: The cleaned string
        """
        return str.replace(' USD', '').replace('$', '').replace('Play Money', '').strip()

    def get_table_bb(self, title):
        """
        From the table`s window title, return the big blinds for such table

        :param title: The title of the window
        :return: The value of the big blind as float
        """
        str = self.get_table_stakes(self.sanitize_string(title))
        return float(str.split('/')[1])

    def get_table_sb(self, title):
        """
        From the table`s window title, return the small blinds for such table

        :param title: The title of the window
        :return: The value of the small blind as float
        """
        str = self.get_table_stakes(self.sanitize_string(title))
        return float(str.split('/')[0])

    def scan_for_tables(self, hwnd_to_scan, scanner, strategy, lobby):
        """
        Scan all the received HWND (Window Handles) in order to check which windows are valid
        PokerStars poker tables.

        :param hwnd_to_scan: List of HWND to scan
        :param scanner: The scanner to use for those tables
        :param strategy: The Strategy to use for those tables.
        :param lobby: The Parent Lobby
        :return: List of PokerTable Instances
        """
        return [PokerTable(x['hwnd'], PokerLobbyPokerStars.get_table_name(x['title']),
                           PokerLobbyPokerStars.get_table_stakes(x['title']),
                           PokerLobbyPokerStars.get_table_format(x['title']),
                           scanner('6-SEATS', 6, self.get_table_bb(x['title']), self.get_table_sb(x['title'])),
                           strategy(), lobby)
                for x in hwnd_to_scan if
                PokerLobbyPokerStars.is_pokerstars_table(x['class'], x['title'])]
