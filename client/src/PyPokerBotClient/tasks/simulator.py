"""
This task analyses a screenshot of a pokertable and then returns a dictionary with
the information captured from such image. It analises the cards on the table, the
hero position and cards and also the commands available to the player.

Usage:
::

    python PyPokerBot.py simulator <Image Source> <Platform> <TableType>


Parameters:

    **Image Source**: The jpg image containing the poker table screenshot to be analysed.

    **Platform**: The Poker Platform (Client Software) that should be considered in the analisys

    **TableType**: The Type of Table, por example, 6-SEAT, 9-SEAT or others.

Return:
    After the analisys is completed, the script prints a friendly representation of the
    returned  dictionary with the following values:

        **Number Of Villains**: Number of Players playing against the Hero

        **Flop**: Current The Cards in the Flop (Table)

    if player is playing current hand:

        **Pocket Cards**: The Cards that the Hero is holding

        **Position**: Current Hero Position in the table

        **Equity**: The Equity (% of success with current hand)

    If there is a decision to be made by the player:

        **Command**: The button to be pressed

        **Decision**: The decision made by the current bot strategy

    Obs:

       * **Hero** is the term used for the current player
       * The python classes to be used for scanning the table and generating the strategy
         are defined in the settings.py file

"""

import os
import os.path
import argparse
import json
import requests

from PyPokerBotClient.utils import get_instance
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.osinterface.image import grab_image_from_file
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute


def usage():
    """Display the current task (simulator) usage

    :return:  None (Prints the usage information to stdout)
    """
    return


"""
This task analyses a screenshot of a pokertable and then returns a dictionary with
the information captured from such image. It analises the cards on the table, the
hero position and cards and also the commands available to the player.

Usage:
    python PyPokerBot.py analyze_table <Image Source> <Platform> <TableType>
Parameters:
    Image Source: The jpg image containing the poker table screenshot to be analysed.
    Platform: The Poker Platform (Client Software) that should be considered in the analisys
    TableType: The Type of Table, por example, 6-SEAT, 9-SEAT or others.

Return:
    After the analisys is completed, the script prints a friendly representation of the
    returned  dictionary with the following values:

    Number Of Villains: Number of Players playing against the Hero
    Flop: Current The Cards in the Flop (Table)

    if player is playing current hand:

    Pocket Cards: The Cards that the Hero is holding
    Position: Current Hero Position in the table
    Equity: The Equity (% of success with current hand)

    If there is a decision to be made by the player:

    Command: The button to be pressed
    Decision: The decision made by the current bot strategy

Obs:
   *Hero is the term used for the current player
   *The python classes to be used for scanning the table and generating the strategy
    are defined in the settings.py file
"""


def get_image_from_folder(image_folder):
    for current_file in os.listdir(image_folder):
        file = os.path.join(image_folder, current_file)
        if os.path.isfile(file):
            yield file


def get_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('image_folder')
    parser.add_argument('image_platform')
    parser.add_argument('image_tabletype')
    parser.add_argument('--observer_url', help='URL to send notifications')
    parser.add_argument(
        '--tableid',
        help='Table ID for Notifications, required if observer_url is set...')
    parser.add_argument('--print_result',
                        help='Print Analisys to STDOUT',
                        default=True)
    options = parser.parse_args(args)
    if (options.tableid is not None and options.observer_url is None) or (
            options.tableid is None and options.observer_url is not None):
        raise ValueError("tableid and observer_url must be BOTH informed")

    should_observe = (options.tableid is not None
                      and options.observer_url is not None)

    return options, should_observe


def clean_string(result):
    result = str(result).replace("\'", "\"").replace('(', '[').replace(
        ')', ']').replace('\\', '|')
    result = result.replace("False", "false")
    result = result.replace("True", "true")
    result = result.replace("[b\"", "[\"")
    result = result.replace(" b\"", " \"")
    return result


def post_table_status(json_result):
    url = Settings.get_table_url() + '/1'
    request_made = requests.post(url, json=json_result)
    if not request_made.status_code == 200:
        print("Error posting status to server...")


def execute(args):
    """Execute is the main entry point for this task module, it receives as parameters the args
    specified on the module description above and run the scanning of the screenshot provided.
    Prints to stdout the contents of the returned python dictionary.

    :param args: The Command Line parameters specified on the module description above which are:
         <Image Source> <Platform> <TableType>

    :return: None (Prints the Analisys to stdout)
    """
    if len(args) < 1:
        print(
            "For this task you need at least 1 arguments: <Image Source> <Platform> <TableType> "
        )
        return

    options, should_observe = get_arguments(args)

    image_folder = options.image_folder
    image_platform = options.image_platform
    image_tabletype = options.image_tabletype
    print_result = options.print_result

    table_scanner_class = get_instance(
        Settings.get_table_scanner_class(image_platform))
    table_strategy_class = get_instance(
        Settings.get_table_strategy_class(image_platform))
    number_of_seats = Settings.get_number_of_seats(image_platform,
                                                   image_tabletype)
    table_scanner = table_scanner_class(image_tabletype, number_of_seats, 0.02,
                                        0.01)
    table_strategy = table_strategy_class()

    for image_name in get_image_from_folder(image_folder):
        table_image = grab_image_from_file(image_name)
        result = table_scanner.analyze_from_image(table_image)
        if has_command_to_execute(result):
            result = table_strategy.run_strategy(result)
        result['image_platform'] = image_platform
        result['image_tabletype'] = image_tabletype
        if print_result:
            final_analisys = ''
            final_analisys += '------------------------------------------------------------\n'
            final_analisys += 'Number of Villains:{}\n'.format(
                len([x for x in result['cards'] if x]))
            final_analisys += '------------------------------------------------------------\n'
            final_analisys += 'Flop              :{}\n'.format("".join(
                result['flop']))
            if 'hero' in result:
                final_analisys += 'Pocket Cards      :{}\n'.format(
                    result['hero']['hero_cards'])
                final_analisys += 'Position          :{}\n'.format(
                    result['hero']['position'])
            else:
                final_analisys += 'HERO is NOT PLAYING...\n'
            if 'hand_analisys' in result:
                final_analisys += 'Equity            :{}\n'.format(
                    result['hand_analisys']['result'])
            else:
                final_analisys += 'NO HAND to Analyse...\n'
            if has_command_to_execute(result):
                final_analisys += '=================================================================\n'
                final_analisys += 'Command           :{}\n'.format(
                    result['commands'][result['command']['to_execute'] - 1])
                final_analisys += 'Decision          :{}({})\n'.format(
                    result['decision']['decision'],
                    result['decision']['raise_strategy'])
                final_analisys += '=================================================================\n'
            PokerTableScanner.generate_analisys_summary_info(final_analisys)
        if should_observe:
            result = clean_string(result)
            json_result = json.dumps(json.loads(result), indent=3)
            post_table_status(json_result)
