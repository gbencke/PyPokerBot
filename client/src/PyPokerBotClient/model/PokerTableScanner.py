"""
This module contains the PokerTableScanner which is the general abstract class
for PokerTable Image scanners
"""
import logging


def has_command_to_execute(analisys):
    """
    This function checks if we have any command to send to the Poker
    Platform UI

    :param analisys: The dictionary returned from a PokerTableScanner instance
    :return: True or False
    """
    return not (
        analisys['commands'][0][0] == '' and
        analisys['commands'][1][0] == '' and
        analisys['commands'][2][0] == '')


class PokerTableScanner(object):
    """
    This is the Abstract class for all poker table image scanners on PokerBot. It
    includes the suits and cards enumerations and some helpful methods.
    """
    suits = ['h', 's', 'c', 'd']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, table_type, number_of_seats, big_blind, small_blind):
        self.table_type = table_type
        self.number_of_seats = number_of_seats
        self.big_blind = big_blind
        self.small_blind = small_blind

    @staticmethod
    def generate_analisys_summary_info(message):
        """
        This method splits a string into lines and then saves the message content as
        lines into the log file

        :param message: Message to be parsed
        :return: None
        """
        for current_message in message.split('\n'):
            logging.info(current_message)
