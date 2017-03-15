import sys
import os
import logging
from importlib import import_module
from settings import settings


def general_configuration():
    current_path = os.getcwd()
    sys.path.append(current_path)
    logging.basicConfig(format=settings['LOG_FORMAT'], level=settings['LOG_LEVEL'])


def show_usage():
    pass


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
