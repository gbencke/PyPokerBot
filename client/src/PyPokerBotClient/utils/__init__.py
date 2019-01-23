# coding=utf-8
"""
Generic utils module to be reused by all python modules.
"""
import importlib


def get_instance(classname):
    """
    Generate a instance of a specific classname and returns it. Used on the task loading
    and also dynamic creation of specific classes like poker strategy classes and table
    analysers.

    :param classname: The name of the classe to be instanciated
    :return: A new instance of the specified classname
    """
    return getattr(importlib.import_module(classname), classname.split('.')[-1])
