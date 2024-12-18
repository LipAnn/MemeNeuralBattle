from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__kb_host_buttons = [
    [
        KeyboardButton(text="Начать игру"),
        KeyboardButton(text="Выйти и завершить игру")
    ]
]
kb_host = ReplyKeyboardMarkup(keyboard=__kb_host_buttons, resize_keyboard=True)
__kb_host_game_buttons = [
    [
        KeyboardButton(text="1"),
        KeyboardButton(text="2"),
        KeyboardButton(text="3"),
    ],
    [
        KeyboardButton(text="4"),
        KeyboardButton(text="5"),
        KeyboardButton(text="6"),
    ],
    [
        KeyboardButton(text="Выйти и завершить игру")
    ]
]
kb_host_game = ReplyKeyboardMarkup(keyboard=__kb_host_game_buttons, resize_keyboard=True)
__kb_client_buttons = [
    [
        KeyboardButton(text="Выйти из игры")
    ]
]
kb_client = ReplyKeyboardMarkup(keyboard=__kb_client_buttons, resize_keyboard=True)
__kb_client_game_buttons = [
    [
        KeyboardButton(text="1"),
        KeyboardButton(text="2"),
        KeyboardButton(text="3"),
    ],
    [
        KeyboardButton(text="4"),
        KeyboardButton(text="5"),
        KeyboardButton(text="6"),
    ],
    [
        KeyboardButton(text="Выйти из игры")
    ]
]
kb_client_game = ReplyKeyboardMarkup(keyboard=__kb_client_game_buttons, resize_keyboard=True)
