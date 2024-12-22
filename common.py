import os

import dotenv
from aiogram import Bot, types

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

images_dir = os.path.dirname("images")
last_image_num = int(os.getenv("LAST_IMAGE_NUM"))


async def update_caches(message: types.Message):
    user_id_to_chat_id[message.from_user.id] = message.chat.id
    first_name = message.from_user.first_name if message.from_user.first_name is not None else ""
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ""
    user_id_to_name[message.from_user.id] = first_name + " " + last_name
