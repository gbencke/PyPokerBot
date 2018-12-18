from PyPokerBotClient.utils import get_instance
from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file
from PyPokerBotClient.model.PokerTableScanner import PokerTableScanner, has_command_to_execute


def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> <Platform> <TableType> ")
        return
    image_name = args[0]
    image_platform = args[1]
    image_tabletype = args[2]

    table_scanner_class = get_instance(Settings.get_table_scanner_class(image_platform))
    table_strategy_class = get_instance(Settings.get_table_strategy_class(image_platform))
    number_of_seats = Settings.get_number_of_seats(image_platform, image_tabletype)
    table_scanner = table_scanner_class(image_tabletype, number_of_seats, 0.02, 0.01)
    table_strategy = table_strategy_class()

    im = grab_image_from_file(image_name)
    result = table_scanner.analyze_from_image(im)
    if has_command_to_execute(result):
        result = table_strategy.run_strategy(result)
        final_analisys = ''
        final_analisys += '====================================\n'
        final_analisys += 'Command           :{}\n'.format(result['commands'][result['command']['to_execute'] - 1])
        final_analisys += 'Decision          :{}({})\n'.format(result['decision']['decision'],
                                                               result['decision']['raise_strategy'])
        final_analisys += '------------------------------------\n'
        final_analisys += 'Number of Villains:{}\n'.format(len([x for x in result['cards'] if x]))
        final_analisys += 'Flop              :{}\n'.format("".join(result['flop']))
        final_analisys += 'Pocket Cards      :{}\n'.format(result['hero']['hero_cards'])
        final_analisys += 'Position          :{}\n'.format(result['hero']['position'])
        final_analisys += 'Equity            :{}'.format(result['hand_analisys']['result'])
        PokerTableScanner.generate_analisys_summary_info(final_analisys)
