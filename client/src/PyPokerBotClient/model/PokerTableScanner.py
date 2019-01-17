import logging


def has_command_to_execute(analisys):
    return not (
            analisys['commands'][0][0] == '' and
            analisys['commands'][1][0] == '' and
            analisys['commands'][2][0] == '')


class PokerTableScanner(object):
    suits = ['h', 's', 'c', 'd']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.BB = BB
        self.SB = SB

    @staticmethod
    def generate_analisys_summary_info(message):
        for x in message.split('\n'):
            logging.info(x)
