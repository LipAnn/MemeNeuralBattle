import os
import random

import requests
import dotenv
import time
import jwt


dotenv.load_dotenv()
service_account_id = os.getenv("YANDEX_SERVICE_ACCOUNT_ID")
key_id = os.getenv("YANDEX_KEY_ID")
private_key = ""
with open("private_key.txt") as file:
    lines = file.readlines()
    for line in lines:
        private_key += line


def get_token():
    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 360}

    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id})

    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    x = requests.post(url, headers={'Content-Type': 'application/json'}, json={'jwt': encoded_token}).json()
    return x['iamToken']


def generate_themes(num):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    data = {}

    data['modelUri'] = 'gpt://b1gg5e92sjuds114h4f0/yandexgpt-lite'

    data['completionOptions'] = {'stream': False,
                                 'temperature': 0.3,
                                 'maxTokens': 1000}

    themes = ["Сын маминой подруги", "Еды", "Бывший или Бывшая", "Любви", "Типичный батя", "Радость", "Школьники",
              "Работа"]
    random.shuffle(themes)
    themes_string = themes[0] + " " + themes[1] + " " + themes[2]

    data['messages'] = [
        {
            "role": "system",
            "text": "Ты являешься креативным директором игры под названием мемы. В этой игре участникам выдается одна общая забавная ситуация, \
                     на которую они пытаются пошутить картинками. Кто будет смешнее, тот и победит. Вам нужно составить список этих \
                     смешных юмористических ситуаций, которые начинаются со слова когда. Ситуации должны быть понятными, \
                     необычными и неожиданными, часто подчеркивающими абсурдность повседневной жизни.\
                     Примеры ситуаций: \
                     1. Когда идешь на свидание, чтобы поесть. \
                     2. Когда все поняли шутку, а ты нет. \
                     3. Когда переслушал свое голосовое сообщение. \
                     4. Когда лег в 6:55, а вставать нужно в 7:00. \
                     5. Когда твой парикмахер говорит: упс. \
                     6. Когда увидел 20 пропущенных от мамы. \
                     7. Когда подобрал пароль к соседскому wifi. \
                     8. Когда водитель такси просит тебя показать дорогу. \
                     9. Когда твою зарплату подняли на 1000 рублей и ты решил посмотреть цены на квартиры. \
                     Учитывай список запретных тем: \
                     1. ключи. \
                     2. утюг. \
                     3. холодильник."
        },
        {
            "role": "user",
            "text": "Создай {num} очень смешных ситуаций на темы: {themes}, которые вызывают смех. \
                     Ситуации должны состоять от 10 до 20 слов".format(themes=themes_string, num=num * 2)
        }
    ]

    result = requests.post(url, headers={'Authorization': 'Bearer ' + get_token()}, json=data).json()
    not_parsed_answer = result["result"]["alternatives"][0]["message"]["text"]
    parsed_answer = not_parsed_answer.split("\n")

    for i in range(1, len(parsed_answer) + 1):
        parsed_answer[i - 1] = parsed_answer[i - 1].removeprefix(str(i) + ". ")

    random.shuffle(parsed_answer)
    return parsed_answer[:num:]
