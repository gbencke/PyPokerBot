from model.PokerLobby import PokerLobby
from model.PokerTable import PokerTable


class PokerLobbyPokerStars(PokerLobby):
    def __init__(self, hwnd, lobby_name):
        PokerLobby.__init__(self)
        self.hwnd = hwnd
        self.lobby_name = lobby_name
        self.tables = []
        self.platform = 'POKERSTARS'

    @staticmethod
    def scan_for_lobbies(hwnd_to_scan):
        ret = []
        for current_hwnd in hwnd_to_scan:
            if PokerLobbyPokerStars.is_pokerstars_lobby(current_hwnd['class'], current_hwnd['title']):
                ret.append(PokerLobbyPokerStars(current_hwnd['hwnd'], current_hwnd['title']))
        return ret

    @staticmethod
    def is_pokerstars_lobby(classname, window_text):
        if 'POKERSTARS LOBBY' in window_text.upper():
            return True

    @staticmethod
    def is_pokerstars_table(classname, window_text):
        if 'PokerStarsTableFrameClass'.upper() in classname.upper():
            return True

    @staticmethod
    def get_table_name(title):
        return title.split('-')[0].strip()

    @staticmethod
    def get_table_stakes(title):
        return title.split('-')[1].strip()

    @staticmethod
    def get_table_format(title):
        return title.split('-')[2].strip()

    def add_tables(self, tables_to_add):
        self.tables += tables_to_add

    def get_tables(self):
        return self.tables

    def sanitize_string(self, str):
        return str.replace(' USD', '').replace('$', '').replace('Play Money', '').strip()

    def get_table_bb(self, title):
        str = self.get_table_stakes(self.sanitize_string(title))
        return float(str.split('/')[1])

    def get_table_sb(self, title):
        str = self.get_table_stakes(self.sanitize_string(title))
        return float(str.split('/')[0])

    def scan_for_tables(self, hwnd_to_scan, scanner, strategy, lobby):
        return [PokerTable(x['hwnd'], PokerLobbyPokerStars.get_table_name(x['title']),
                           PokerLobbyPokerStars.get_table_stakes(x['title']),
                           PokerLobbyPokerStars.get_table_format(x['title']),
                           scanner('6-SEATS', 6, self.get_table_bb(x['title']), self.get_table_sb(x['title'])),
                           strategy(), lobby)
                for x in hwnd_to_scan if
                PokerLobbyPokerStars.is_pokerstars_table(x['class'], x['title'])]
