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
