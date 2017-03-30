from flask import Flask, request
import pbots_calc
from helpers.RangeHelper import RangeHelper
from helpers.LookupTable import LookupTable
import lookup_table

app = Flask(__name__)
lookup_table_utils = LookupTable()

def normalize_cards(tokens):
    start_cards = (RangeHelper()).parse(tokens[0])
    start_cards = lookup_table_utils.rearrange_cards(start_cards)
    start_cards_list = tokens[0].split(':')
    start_cards_list[0] = start_cards.split(':')[0]
    start_cards = ':'.join(start_cards_list)
    return start_cards

@app.route('/calculator', methods=['POST'])
def calculator():
    command = request.get_json()['command']
    tokens = command.split(' ')
    start_cards = normalize_cards(tokens)
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
    for x in lookup_table.lookup_table.keys():
        print(str(lookup_table.lookup_table[x])[:80])
        card_found = filter(lambda card: card['cards'] == start_cards, lookup_table.lookup_table[x])
        print(card_found)
        if len(card_found) > 0:
            return str([(start_cards,card_found[0]['equity'])])
    print("{} not found in lookup_tables".format(start_cards))
    r = pbots_calc.calc(start_cards, board, dead, 1000000)
    if r:
        return str(zip(r.hands, r.ev))

