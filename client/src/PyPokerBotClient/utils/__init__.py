# coding=utf-8
import importlib


def get_instance(classname):
    return getattr(importlib.import_module(classname), classname.split('.')[-1])
