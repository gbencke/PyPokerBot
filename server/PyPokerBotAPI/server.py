import sys
from flask import Flask, request

sys.path.insert(0, ".")

from calculator.pbots_calc import calc
from helpers.RangeHelper import RangeHelper
from helpers.LookupTable import LookupTable
from lookup_table.lookup_table import lookup_table

app = Flask(__name__)
lookup_table_utils = LookupTable()

table_status = {}


def normalize_cards(tokens):
    start_cards = (RangeHelper()).parse(tokens[0])
    start_cards = lookup_table_utils.rearrange_cards(start_cards)
    start_cards_list = tokens[0].split(':')
    start_cards_list[0] = start_cards.split(':')[0]
    start_cards = ':'.join(start_cards_list)
    return start_cards


@app.route('/table/<tableid>', methods=['POST'])
def table(tableid):
    str_tableid = str(tableid)
    table_status[str_tableid] = request.get_json()
    print("Status for table:{} was received".format(tableid))
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
            print(str(lookup_table[x])[:80])
            card_found = list(
                filter(lambda card: card['cards'] == start_cards,
                       lookup_table[x]))
            print(card_found)
            if len(card_found) > 0:
                print("Found {} in lookup_table".format(start_cards))
                return str([(start_cards, card_found[0]['equity'])])
        print("{} not found in lookup_tables".format(start_cards))
    print("{} {} {} will be calculated".format(start_cards, board, dead))
    r = calc(start_cards, board, dead, 1000000)
    if r:
        print("{} calculated equity:{}".format(start_cards, str(r.ev)))
        return str((r.hands, r.ev))
    else:
        print("Error for:{}".format(r))
        return "Error"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
