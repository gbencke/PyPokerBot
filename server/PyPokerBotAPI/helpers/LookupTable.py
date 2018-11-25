import sys
import pprint
from calculator.pbots_calc import calc

class LookupTable:

    suits = ['h','s','c','d']
    cards = { '2' : 2, 
            '3' : 3,
            '4' : 4,
            '5' : 5,
            '6' : 6,
            '7' : 7,
            '8' : 8,
            '9' : 9,
            'T' : 10,
            'J' : 11,
            'Q' : 12,
            'K' : 13,
            'A' : 14 
          }

    def __init__(self):
        pass

    def rearrange_cards(self,current_card_set):
        if LookupTable.cards[current_card_set[2]] > LookupTable.cards[current_card_set[0]]:
            current_card_set = current_card_set[2:3] + current_card_set[3:4] + current_card_set[0:1] + current_card_set[1:2]
            return current_card_set
        if current_card_set[1] > current_card_set[3] and current_card_set[0] == current_card_set[2]:
            current_card_set = current_card_set[2:3] + current_card_set[3:4] + current_card_set[0:1] + current_card_set[1:2]
            return current_card_set
        return current_card_set


    def calculate_total_stats(self,list_to_calculate):
        total=len(list_to_calculate)
        current = 0
        for k in list_to_calculate:
            list_to_calculate[current]['rank'] = (float(current) / float(total)) * 100
            list_to_calculate[current]['total'] = total
            list_to_calculate[current]['current'] = current
            current += 1
        return list_to_calculate


    def create_lookup(self, villains):
        ret = { }
        for c_suit_card_1 in LookupTable.suits:
            for c_card_card_1 in LookupTable.cards:
                for c_suit_card_2 in LookupTable.suits:
                    for c_card_card_2 in LookupTable.cards:
                        current_cards = c_card_card_1 + c_suit_card_1 + \
                                c_card_card_2 + c_suit_card_2
                        if current_cards[0:2] == current_cards[2:]:
                            continue
                        current_cards = self.rearrange_cards(current_cards)
                        if current_cards in ret:
                            continue
                        print('#{}'.format(current_cards))
                        sys.stdout.flush()
                        ret[current_cards] = \
                            { "cards" : current_cards + ":" + villains, 
                              "equity": calc(current_cards + ":" + villains, "", "", 1000000).ev[0] }
        ret_list = [ {'cards': ret[x]['cards'], 'equity': ret[x]['equity']} for x in ret.keys()]
        ret_list = sorted(ret_list, key=lambda k:k['equity'], reverse = True)
        return self.calculate_total_stats(ret_list)




