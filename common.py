import os

import dotenv
from aiogram import Bot

dotenv.load_dotenv()

token = os.getenv("TOKEN")
bot = Bot(token)

game_code_to_host_dict = dict()
host_to_game_code = dict()
code_to_game = dict()
action = dict()
user_id_to_chat_id = dict()
user_id_to_name = dict()
used_codes = list()
