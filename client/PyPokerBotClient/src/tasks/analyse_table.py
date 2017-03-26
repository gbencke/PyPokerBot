import ast
import numpy
import cv2
import pprint
import subprocess
import requests
import os
import logging
from datetime import datetime
from time import sleep
from settings import settings
from os.win32.screenshot import grab_image_from_file, grab_image_pos_from_image






def generate_analisys(im):
    result = {'seats': 6, 'cards': analyse_players_with_cards(im), 'nocards': analyse_players_without_cards(im)}
    result['button'] = analyse_button(im)
    result['hero'] = analyse_hero(im, result['cards'], result['nocards'], result['button'])
    result['flop'] = analyse_flop_template(im)
    result['commands'] = analyse_commands(im)
    if has_command_to_execute(result):
        result['hand_analisys'] = analyse_hand(result)
        result['decision'] = generate_decision(result)
        result['command'] = generate_command(result)
    return result


def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> ")
        return
    image_name = args[0]
    im = grab_image_from_file(image_name)
    result = generate_analisys(im)
    pprint.PrettyPrinter().pprint(result)
