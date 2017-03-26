import importlib
from settings import settings
import pprint
from osinterface.win32.screenshot import grab_image_from_file


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
    table_scanner = table_scanner_class(image_tabletype)
    table_strategy = table_strategy_class()

    im = grab_image_from_file(image_name)
    result = table_scanner.analyze_from_image(im)
    result = table_strategy.run_strategy(result)
    pprint.PrettyPrinter().pprint(result)
