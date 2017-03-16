from flask import Flask, request
import pbots_calc
from helpers.RangeHelper import RangeHelper

app = Flask(__name__)

@app.route('/calculator', methods=['POST'])
def calculator():
    command = request.get_json()['command']
    tokens = command.split(' ')
    start_cards=(RangeHelper()).parse(tokens[0])
    board = ""
    dead = ""
    if len(tokens) > 1:
        board = tokens[1]
    if len(tokens) > 2:
        dead = tokens[2]
    r = pbots_calc.calc(start_cards, board, dead, 1000000)
    if r:
        return str(zip(r.hands, r.ev))
