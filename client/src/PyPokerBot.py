"""This module is the main CLI interface to the PokerBot. It runs through a
lot of 'tasks' that can be shown by calling this module without arguments.
This is the main interface to the bot.
"""
import sys
import os
import logging
import pkgutil

from datetime import datetime
from importlib import import_module

from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
import PyPokerBotClient.tasks as tasks


def general_configuration():
    """ Performs the general configuration of the bot like setting
    the correct working directory and also loading the logging
    configurations...
    """
    current_path = os.getcwd()
    sys.path.append(current_path)
    logging.basicConfig(format=Settings.get_log_format(),
                        level=Settings.get_log_level(),
                        filename=os.path.join(Settings.get_log_location(),
                                              'log.' + datetime.now().strftime("%Y%m%d%H%M%S.%f")
                                              + '.log'))
    logging.getLogger().addHandler(logging.StreamHandler())


def show_usage():
    """Scans through the tasks module and show the tasks that are available and
    their required command-line parameters.
    """
    print("Welcome to PyPokerBot")
    print("=====================")
    print("Please execute: python PyPokerBot.py <task to run> [arguments]* ")
    print("Currently available tasks:")
    tasks_available = [modname for _, modname, _ in pkgutil.iter_modules(tasks.__path__)]
    for current_task in tasks_available:
        try:
            module_to_import = "PyPokerBotClient.tasks." + current_task
            mod = import_module(module_to_import)
            method_to_call = "usage"
            method_pointer = getattr(mod, method_to_call)
            descricao = method_pointer()
            print("-{}:{}\n".format(current_task, descricao))
        except ImportError as exception_raised:
            logging.debug("command ({0}) tried to import: {1} {2}".format(
                current_task, module_to_import, exception_raised))
            continue


def process_command(args):
    """Parses the command line parameters and then load the correct task module to run it.
    It is important to notice that the first command line parameter is the name of the
    module to be used.
    """
    module_to_import = "PyPokerBotClient.tasks." + args[0]
    try:
        mod = import_module(module_to_import)
    except ImportError as exception_raised:
        logging.debug(
            "Error, this command ({0}) was not found, tried to import: {1} {2}".format(
                args[0], module_to_import, exception_raised))
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
