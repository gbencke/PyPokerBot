# coding=utf-8
from PyPokerBotClient.settings.default_settings import settings as default_setting


class Settings:

    def __init__(self):
        pass

    def get_log_format(self):
        return default_setting['LOG_FORMAT']

    def get_log_level(self):
        return default_setting['LOG_LEVEL']

    def get_log_location(self):
        return default_setting['LOG_LOCATION']

    def get_table_scanner_class(self, image_platform):
        return default_setting['PLATFORMS'][image_platform]['POKER_TABLE_SCANNER_CLASS']

    def get_table_strategy_class(self, image_platform):
        return default_setting['PLATFORMS'][image_platform]['POKER_STRATEGY_CLASS']

    def get_number_of_seats(self, image_platform, image_tabletype):
        return default_setting['PLATFORMS'][image_platform]['TABLE_SCANNER'][image_tabletype]['NUMBER_OF_SEATS']

    def get_calculate_url(self):
        return default_setting['STRATEGIES']['SIMPLE']['CALCULATE_URL']

    def get_player_hasnocard_template(self, platform, index):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][
                   'TEMPLATES_FOLDER'] + '\\' + 'PLAYER{}_HASNOCARD'.format(index + 1) + '.jpg'

    def get_button_template(self, platform, index):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][
                   'TEMPLATES_FOLDER'] + '\\' + 'BUTTON{}_TEMPLATE'.format(index + 1) + '.jpg'

    def get_card_template(self, platform, current_card, current_suit):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][
                   'TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'

    def get_nobet_template(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['NOBET_TEMPLATE']

    def get_flopcard(self, platform, tabletype, index):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
            'FLOPCARD{}'.format(index + 1)]

    def get_flopcard_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['FLOPCARD_SIZE']

    def get_flop_card_key(self, platform, tabletype, flop_card_key):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][flop_card_key],

    def get_command_current_pos_key(self, platform, tabletype, current_pos_key):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][current_pos_key],

    def get_command_test_tolerance(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['COMMAND_TEST_TOLERANCE']

    def get_command_test_template(self, platform, tabletype, current_command):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
            'COMMAND_TEST_TEMPLATE{}'.format(current_command)]

    def get_command_test_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['COMMAND_TEST_SIZE']

    def get_command_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['COMMAND_SIZE']

    def get_button(self, platform, tabletype, index):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
                   'BUTTON{}'.format(index + 1)],

    def get_button_threshold(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['BUTTON_THRESHOLD']

    def get_button_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['BUTTON_SIZE']

    def get_player_has_unknown_card_template(self, platform):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER']['PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']

    def get_comand_pos(self, platform, tabletype, current_command):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
            'COMMAND_POS{}'.format(current_command)]

    def get_flop_has_nocard_template(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
            'FLOPCARD_HAS_NOCARD_TEMPLATE']

    def get_play_hascard_threshold(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['PLAY_HASCARD_THRESHOLD']

    def get_player_hascard(self, platform, tabletype, index):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['PLAYER{}_HASCARD'.format(index + 1)]

    def get_template(self, platform, tabletype, template):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype][
            '{}_TEMPLATE'.format(template)]

    def get_bet_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['BET_SIZE']

    def get_bet(self, platform, tabletype, x):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['BET{}'.format(x + 1)]

    def get_playerhascard_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['PLAYERHASCARD_SIZE']

    def get_command_pos(self, platform, tabletype, pos):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['COMMAND_POS{}'.format(pos + 1)],

    def get_pot(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['POT']

    def get_pot_size(self, platform, tabletype):
        return default_setting['PLATFORMS'][platform]['TABLE_SCANNER'][tabletype]['POT_SIZE']

