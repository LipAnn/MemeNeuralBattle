import os
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


def get_generated_themes(num):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    data = {}

    data['modelUri'] = 'gpt://b1gg5e92sjuds114h4f0/yandexgpt-lite'

    data['completionOptions'] = {'stream': False,
                                 'temperature': 0.3,
                                 'maxTokens': 1000}

    data['messages'] = [
        {
            "role": "system",
            "text": "   ты — продвинутая языковая модель, способная генерировать короткие остроумные истории для игры, у которой прекрасное чувство юмора. Для этой игры участникам выдается одна смешная ситуация, \
                        над которой они пытаются пошутить картинками, у них на руках. Побеждает тот, у которого картинка смешнее подходит к ситуации. \
                        Тебе нужно будет придумывать эти кринжовые ситуации, иногда абсурдные. Важно, чтобы ситуации были короткими и смешными. Вот примеры ситуаций \
                        1. Когда идешь на свидание, чтобы поесть. \
                        2. Когда все поняли шутку, а ты нет. \
                        3. Когда переслушал свое голосовое сообщение. \
                        4. Когда лег в 6:55, а вставать нужно в 7:00. \
                        5. Когда твой парикмахер говорит: упс. \
                        6. Когда увидел 20 пропущенных от мамы. \
                        7. Когда мама говорит: Делай что хочешь. \
                        8. Когда подобрал пароль к соседскому wifi. \
                        9. Когда водитель такси просит тебя показать дорогу. \
                        10. Когда твою зарплату подняли на 1000 рублей и ты решил посмотреть цены на квартиры."
        },
        {
            "role": "user",
            "text": "Сгенерируй {num} смешных очень коротких кринжовых абсурдных ситуаций на тему работы, начиная со слов когда. Используй разнообразные вводные данные, чтобы ситуации были максимально разнообразными и неожиданными и вызывали улыбку у игроков.".format(num=num * 2)
        }
    ]

    result = requests.post(url, headers={'Authorization': 'Bearer ' + get_token()}, json=data).json()
    not_parsed_answer = result["result"]["alternatives"][0]["message"]["text"]
    parsed_answer = not_parsed_answer.split("\n")

    for i in range(1, len(parsed_answer) + 1):
        parsed_answer[i - 1] = parsed_answer[i - 1].removeprefix(str(i) + ". ")

    return parsed_answer[:num:]
