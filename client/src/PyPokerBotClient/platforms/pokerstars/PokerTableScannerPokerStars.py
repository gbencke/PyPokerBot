# coding=utf-8
"""
This Module contains the class used for the scanning of the poker table being played, it is
configured on the settings.py file and passed as a argument to the table instance created by the
table lobby.
"""
import re

from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute
from PyPokerBotClient.platforms.utils import create_list_seats
from PyPokerBotClient.custom_exceptions import NeedToSpecifySeatsException, \
    NeedToSpecifyTableTypeException
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalysePlayersWithCards import \
    PokerAnalysePlayersWithCards
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalysePlayersWithoutCards \
    import PokerAnalysePlayersWithoutCards
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseCommands \
    import PokerAnalyseCommands
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseButton \
    import PokerAnalyseButton
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseFlop \
    import PokerAnalyseFlop
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseHero \
    import PokerAnalyseHero
from PyPokerBotClient.platforms.pokerstars.image_scanner.PokerAnalyseHand \
    import PokerAnalyseHand


class PokerTableScannerPokerStars(PokerTableScanner):
    """
    The PokerBot is a software that when is in **Play** mode, enters a loop and
    creates screenshots of a single poker table from a certain Poker platform
    like: 888 poker, PokerStars, and many others. The main problem is that the
    screenshot is just a picture, so it is very hard to analyse it as we do in
    any text-based software, so we neede to use Computer Vision Techniques to turn the image into
    a text-based representation of the current status of the poker table.

    The Analysis of the Poker Table based on a image is quite hard, because we need to
    understand what we need to see and what image is relevant in comparison to another.
    Mainly the information that we need is

    * **Analyse Commands**: Analyse the current commands available to the PokerBot (Hero)
    * **Analyse which Player has cards**: Check if a certain player on the table is
        participating on the current hand, he has cards
    * **Analyse which Player doesn`t have cards**: Check if a certain player is not
        participating on the current hand
    * **Analyse the Button**: Check which Players has the button
    * **Analyse the Flop**: Check which cards are on the table`s flop (the common cards)
    * **Analyse the Hero**: Check which cards are available to the player (If the hero has cards)
    * **Analyse the Hero`s Equity**: With the cards available to the player and the common cards
      (Flop), we check the probability of having the best hand, if the hero has cards.

    For each one of the analysis above, there is a class that handles the specifics for
    such analysis. The PokerTableScannerPokerStars aggregates such small classes and provide a
    final dictionary with the final analisys
    """

    def __init__(self, table_type, number_of_seats, big_blind, small_blind):
        """
        Constructor for the table scanner, it takes as parameter, the table type
        (6-SEAT, 9-SEAT), the number of seats, and the value of the small blind and the big blind.

        This class only scans images from Pokerstars platform tables.
        It instatiates the child scanners that scan the specific aspects of each table.

        :param table_type: The TableType for this scanner, if this is a 6-SEAT or 9-SEAT
            for example as defined on
            the settings.py file
        :param NumberOfSeats: The Number of Seats on that table.
        :param BB: The Value of the BigBlind
        :param SB: The Value of the SmallBlind
        """
        PokerTableScanner.__init__(self, table_type, number_of_seats, big_blind, small_blind)
        self.platform = 'POKERSTARS'
        self.flop_size = 5
        self.button_template_histogram = create_list_seats(self.number_of_seats)
        self.player_button_threshold = None
        self.non_decimal = re.compile(r'[^\d.]+')
        self.analyse_command = PokerAnalyseCommands(self.platform, self.table_type, self.big_blind)
        self.analyse_players_with_cards = PokerAnalysePlayersWithCards(
            self.platform,
            self.table_type,
            self.number_of_seats)
        self.analyse_players_without_cards = PokerAnalysePlayersWithoutCards(
            self.platform,
            self.table_type,
            self.number_of_seats)
        self.analyse_button = PokerAnalyseButton(
            self.platform,
            self.table_type,
            self.number_of_seats)
        self.analyse_flop = PokerAnalyseFlop(
            self.platform,
            self.table_type,
            self.number_of_seats,
            self.flop_size)
        self.analyse_hero = PokerAnalyseHero(
            self.platform,
            self.table_type,
            self.number_of_seats)
        self.analyse_hand = PokerAnalyseHand(
            self.platform,
            self.table_type,
            self.number_of_seats,
            self.flop_size)

    @staticmethod
    def has_command_to_execute(analisys):
        """
        Check if the hero has a command to execute on the poker client based on the
        analisys dictionary passed as parameter

        :param analisys: The Dictionary containing the analisys of the screenshot
            of the poker client table.
        :return: True (Needs a Command) or False (Doesn`t need a command)
        """
        return has_command_to_execute(analisys)

    def analyze_from_image(self, image_to_analyse):
        """
        This the main method for the Table Scanner Class as it takes as argument a image,
        and returns a dictionary with the analisys for the table status. Such dictionary
        can be used as input for a Poker Strategy class that will then return the best strategy
        for the specific situation shown on the input image. Such analisys is as follows:

::

            ------------------------------------------------------------
            Number of Villains:2
            ------------------------------------------------------------
            Flop              :
            Pocket Cards      :5sKh
            Position          :BB
            Equity            :[(u'Kh5s:XX', 0.5336055)]
            =================================================================
            Command           :('FOLD', '', 'Fold ')
            Decision          :FOLD OR CHECK(0)
            =================================================================

The above Represents:

* *seats*: The number of seats on the table
* *commands*: The current available buttons to be pressed on the Poker Client UI
* *cards*: A List of Booleans indicating if a certain position has a playing card
* *nocards*: A List of Booleans indicating if a certain position has no playing card.
* *button*: A List of Booleans indicating if a certain position has the button.
* *flop*: The flop cards shown on the table
* *hero*: The Cards that the Hero (Player) has on his pocket
* *hand_analisys*: The probability of the Pocket Cards and the Flop cards being the winning hand

:param im: A Screenshot of a pokerstars table
:return: Dictionary with the analisys of the table.
        """
        if self.number_of_seats is None:
            raise NeedToSpecifySeatsException \
                ('You need to specify the number of seats prior to start analisys')
        if self.table_type is None:
            raise NeedToSpecifyTableTypeException \
                ('You need to specify the table type prior to start analisys')
        result = {}
        result['seats'] = self.number_of_seats
        result['commands'] = self.analyse_command.analyse_commands(image_to_analyse)
        result['cards'] = self.analyse_players_with_cards.analyse_players_with_cards(
            image_to_analyse)
        result['nocards'] = \
            self.analyse_players_without_cards.analyse_players_without_cards(
                image_to_analyse)
        result['button'] = self.analyse_button.analyse_button(image_to_analyse)
        result['flop'] = self.analyse_flop.analyse_flop_template(image_to_analyse)
        if has_command_to_execute(result):
            result['hero'] = self.analyse_hero.analyse_hero(
                image_to_analyse,
                result['cards'],
                result['nocards'],
                result['button'])
            result['hand_analisys'] = self.analyse_hand.analyse_hand(result)
        return result
