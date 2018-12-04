import sys
import os
import logging
import pkgutil

from datetime import datetime
from importlib import import_module

from settings import settings
import PyPokerBotClient.tasks as tasks


def general_configuration():
    current_path = os.getcwd()
    sys.path.append(current_path)
    logging.basicConfig(format=settings['LOG_FORMAT'],
                        level=settings['LOG_LEVEL'],
                        filename=os.path.join(settings['LOG_LOCATION'],
                                              'log.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + '.log'))
    logging.getLogger().addHandler(logging.StreamHandler())


def show_usage():
    print("Welcome to PyPokerBot")
    print("=====================")
    print("Please execute: python PyPokerBot.py <task to run> [arguments]* ")
    print("Currently available tasks:")
    tasks_available = [modname for importer, modname, ispkg in pkgutil.iter_modules(tasks.__path__)]
    for current_task in tasks_available:
        print("-{}".format(current_task))


def process_command(args):
    module_to_import = "tasks." + args[0]
    try:
        mod = import_module(module_to_import)
    except ImportError, e:
        logging.debug(
            "Error, this command ({0}) was not found, tried to import: {1} {2}".format(args[0], module_to_import, e))
        return
    arguments_for_method_to_call = args[1:]
    method_to_call = "execute"
    method_pointer = getattr(mod, method_to_call)
    method_pointer(arguments_for_method_to_call)


if __name__ == '__main__':
    general_configuration()
    if len(sys.argv) == 1:
        show_usage()
    else:
        process_command(sys.argv[1:])
