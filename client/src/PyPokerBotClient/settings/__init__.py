# coding=utf-8
"""
This is the module that controls the global settings of the PokerBot, as being loaded, it instanciates
a singleton for the Settings() class and returns it to the other modules of the bot.
"""
from PyPokerBotClient.settings.Settings import Settings

"""
Global Settings Singleton
"""
GlobalSettings = Settings()
