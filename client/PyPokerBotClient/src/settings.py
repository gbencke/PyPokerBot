settings = {
    "LOG_LEVEL": "DEBUG",
    "LOG_FORMAT": "%(asctime)-15s %(message)s",
    "LOG_LOCATION": "..\..\logs",
    "SAMPLES_FOLDER": "..\..\data",
    "SLEEP_TIME_BETWEEN_CAPTURE_MS": 100,

    "STRATEGY": {
        "CALCULATE_URL": "http://192.168.198.134:5000/calculator",
        "PREFLOP": {
            "CONFIDENCE_LEVEL": 0.6,
            "PLAYER_STRENGTH": "XX"
        },
        "FLOP": {
            "CONFIDENCE_LEVEL": 0.6,
            "PLAYER_STRENGTH": "T5"
        }
    },

    "TABLE_SCANNER": {
        "TEMPLATES_FOLDER": "..\..\data\\template",
        "TABLE_SIZE": (614, 456),
        "PLAYERCARD_HAS_NOCARD_TEMPLATE": "",
        "PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE": "..\..\data\\template\PLAYER_HASCARD.jpg",

        "PLAYERHASCARD_SIZE": (162, 42),
        "PLAY_HASCARD_THRESHOLD": 0.90,
        "PLAYER1_HASCARD": (1056, 194),
        "PLAYER2_HASCARD": (1056, 473),
        "PLAYER3_HASCARD": (571, 629),
        "PLAYER4_HASCARD": (92, 473),
        "PLAYER5_HASCARD": (92, 194),
        "PLAYER6_HASCARD": (574, 88),

        "PLAYERCARD11_POS": (1060, 176),
        "PLAYERCARD12_POS": (1138, 176),
        "PLAYERCARD21_POS": (1060, 454),
        "PLAYERCARD22_POS": (1138, 454),
        "PLAYERCARD31_POS": (575, 610),
        "PLAYERCARD32_POS": (651, 610),
        "PLAYERCARD41_POS": (95, 454),
        "PLAYERCARD42_POS": (173, 454),
        "PLAYERCARD51_POS": (95, 176),
        "PLAYERCARD52_POS": (173, 176),
        "PLAYERCARD61_POS": (575, 79),
        "PLAYERCARD62_POS": (653, 79),

        "FLOPCARD_SIZE": (60, 50),
        "FLOPCARD_HAS_NOCARD_TEMPLATE": "..\..\data\\template\NOFLOP.jpg",
        "FLOPCARD1": (455, 356),
        "FLOPCARD2": (536, 356),
        "FLOPCARD3": (617, 356),
        "FLOPCARD4": (698, 356),
        "FLOPCARD5": (779, 356),

        "BUTTON_SIZE": (39, 34),
        "BUTTON_THRESHOLD": 0.90,
        "BUTTON_TEMPLATE": "..\..\data\\template\BUTTON.jpg",
        "BUTTON1": (999, 321),
        "BUTTON2": (944, 527),
        "BUTTON3": (742, 585),
        "BUTTON4": (317, 527),
        "BUTTON5": (278, 313),
        "BUTTON6": (537, 228),

        "COMMAND_TEST_SIZE": (20, 20),
        "COMMAND_SIZE": (180, 65),
        "COMMAND_TEST_TOLERANCE": 0.90,
        "COMMAND_POS1": (642, 847),
        "COMMAND_POS2": (863, 847),
        "COMMAND_POS3": (1081, 847),

        "COMMAND_TEST_TEMPLATE1": "..\..\data\\template\COMMAND_TEST_TEMPLATE1.jpg",
        "COMMAND_TEST_TEMPLATE2": "..\..\data\\template\COMMAND_TEST_TEMPLATE2.jpg",
        "COMMAND_TEST_TEMPLATE3": "..\..\data\\template\COMMAND_TEST_TEMPLATE3.jpg",

    }
}
