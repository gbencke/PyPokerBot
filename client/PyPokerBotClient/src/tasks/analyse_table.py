import importlib
from settings import settings
from osinterface.win32.screenshot import grab_image_from_file
from model.PokerTableScanner import PokerTableScanner


def get_instance(classname):
    return getattr(importlib.import_module(classname), classname.split('.')[-1])


def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> <Platform> <TableType> ")
        return
    image_name = args[0]
    image_platform = args[1]
    image_tabletype = args[2]
    table_scanner_class = get_instance(settings['PLATFORMS'][image_platform]['POKER_TABLE_SCANNER_CLASS'])
    table_strategy_class = get_instance(settings['PLATFORMS'][image_platform]['POKER_STRATEGY_CLASS'])
    number_of_seats = (settings['PLATFORMS'][image_platform]['TABLE_SCANNER'][image_tabletype]['NUMBER_OF_SEATS'])
    table_scanner = table_scanner_class(image_tabletype, number_of_seats, 0.02, 0.01)
    table_strategy = table_strategy_class()

    im = grab_image_from_file(image_name)
    result = table_scanner.analyze_from_image(im)
    result = table_strategy.run_strategy(result)
    final_analisys = ''
    final_analisys += '====================================\n'
    final_analisys += 'Command           :{}\n'.format(result['commands'][result['command']['to_execute'] - 1])
    final_analisys += 'Decision          :{}\n'.format(result['decision']['decision'])
    final_analisys += '------------------------------------\n'
    final_analisys += 'Number of Villains:{}\n'.format(len([x for x in result['cards'] if x]))
    final_analisys += 'Flop              :{}\n'.format("".join(result['flop']))
    final_analisys += 'Pocket Cards      :{}\n'.format(result['hero']['hero_cards'])
    final_analisys += 'Position          :{}\n'.format(result['hero']['position'])
    final_analisys += 'Equity            :{}'.format(result['hand_analisys']['result'])
    PokerTableScanner.generate_analisys_summary(final_analisys)



