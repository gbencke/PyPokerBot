import os
import logging
import sys
from datetime import datetime

from flask_cors import CORS
from flask import Flask, request
from flask_socketio import SocketIO

sys.path.insert(0, ".")

from calculator.pbots_calc import calc
from helpers.RangeHelper import RangeHelper
from helpers.LookupTable import LookupTable
from lookup_table.lookup_table import lookup_table
from settings import settings

app = Flask(__name__)
CORS(app)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000
app.config['SECRET_KEY'] = '12345'

log_location = os.path.join(
    os.getcwd(), settings['LOG_LOCATION'],
    'server.' + datetime.now().strftime('%Y%m%d%H%M%S.%f') + '.log')
print('log_location:{}'.format(log_location))
logging.basicConfig(format=settings['LOG_FORMAT'],
                    level=settings['LOG_LEVEL'],
                    filename=log_location)
#logging.getLogger().addHandler(logging.StreamHandler())

socketio = SocketIO(app)
lookup_table_utils = LookupTable()

table_status = {}


def normalize_cards(tokens):
    start_cards = (RangeHelper()).parse(tokens[0])
    start_cards = lookup_table_utils.rearrange_cards(start_cards)
    start_cards_list = tokens[0].split(':')
    start_cards_list[0] = start_cards.split(':')[0]
    start_cards = ':'.join(start_cards_list)
    return start_cards


@app.route('/ping', methods=['GET'])
def ping():
    return "PONG"


@app.route('/table/<tableid>', methods=['POST'])
def table(tableid):
    str_tableid = str(tableid)
    table_status[str_tableid] = request.get_json()
    logging.debug("Status for table:{} was received".format(tableid))
    logging.debug(table_status[str_tableid])
    socketio.emit('tablestatus', table_status[str_tableid])
    return "OK"


@app.route('/calculator', methods=['POST'])
def calculator():
    command = request.get_json()['command']
    tokens = command.split(' ')
    start_cards = tokens[0]
    board = ""
    dead = ""
    if len(tokens) > 1:
        board = tokens[1]
    else:
        board = ''
    if len(tokens) > 2:
        dead = tokens[2]
    else:
        dead = ''
    if board == "":
        start_cards = normalize_cards(tokens)
        for x in lookup_table.keys():
            logging.debug(str(lookup_table[x])[:80])
            card_found = list(
                filter(lambda card: card['cards'] == start_cards,
                       lookup_table[x]))
            logging.debug(card_found)
            if len(card_found) > 0:
                logging.debug("Found {} in lookup_table".format(start_cards))
                return str([(start_cards, card_found[0]['equity'])])
        logging.debug("{} not found in lookup_tables".format(start_cards))
    logging.debug("{} {} {} will be calculated".format(start_cards, board,
                                                       dead))
    r = calc(start_cards, board, dead, 1000000)
    if r:
        logging.debug("{} calculated equity:{}".format(start_cards, str(r.ev)))
        return str((r.hands, r.ev))
    else:
        logging.debug("Error for:{}".format(r))
        return "Error"


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
