import random
import time

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import common
import default_menu
import replies
import tg_utils
import ya_gpt
from keyboard import kb_host_game, kb_client_game, kb_host, kb_client

games = list()


class Game:

    def __init__(self, code, host, limit_players):
        self.code = code
        self.host = host
        self.limit_players = limit_players
        self.players = list()
        self.is_started = False
        self.round = 0
        self.themes = list()
        self.player_images = dict()
        self.round_limit = 5
        self.answer = dict()
        self.user_id_to_answer_order = dict()
        self.round_finished = dict()
        self.last_used_card_index = dict()
        self.vote = dict()
        self.vote_finished = dict()
        self.scoreboard = dict()
        self.user_index_to_picture_number = list()
        self.picture_number_to_user_index = list()
        self.ai = True
        self.is_break = True

        self.players.append(host)
        common.host_to_game_code[host] = code
        common.game_code_to_host_dict[code] = host
        common.code_to_game[code] = self
        common.used_codes.append(self.code)

        games.append(self)

    async def send_to_players(self, message):
        await tg_utils.send_group_message(self.players, message)

    async def send_to_players_kb(self, message, keyboard):
        await tg_utils.send_group_message_kb(self.players, message, keyboard)

    async def join(self, player):

        self.players.append(player)

        for current_player in self.players:
            await tg_utils.send_message(current_player,
                                        replies.PLAYER_JOINED_TO_HOST_MESSAGE
                                        .format(name=common.user_id_to_name[player]) + "\n" +
                                        replies.PLAYER_COUNT
                                        .format(cur=len(self.players), limit=self.limit_players))

    async def leave(self, player):
        self.players.remove(player)

        for current_player in self.players:
            await tg_utils.send_message(current_player,
                                        replies.PLAYER_LEFT_THE_GAME
                                        .format(name=common.user_id_to_name[player]) + "\n" +
                                        replies.PLAYER_COUNT
                                        .format(cur=len(self.players), limit=self.limit_players))

    async def is_player(self, player):
        return self.players.__contains__(player)

    async def is_host(self, player):
        return self.host == player

    async def destroy(self):
        for player in self.players:
            common.action[player] = ""
            await tg_utils.send_message_kb(player, replies.THE_GAME_HAS_BEEN_DESTROYED, default_menu.kb_default)

        self.players.clear()
        del common.host_to_game_code[self.host]
        del common.code_to_game[self.code]
        del common.game_code_to_host_dict[self.code]
        common.used_codes.remove(self.code)
        games.remove(self)

    @staticmethod
    async def get_game(player):
        for game in games:
            if game.players.__contains__(player):
                return game
        return None

    @staticmethod
    async def is_in_game(player):
        return False if await Game.get_game(player) is None else True

    async def prepare_game(self):
        self.round = 0

        if not self.ai:
            with open("themes/themes.txt", encoding="UTF-8") as themes_file:
                themes = themes_file.readlines()
            for i in range(self.round_limit):
                theme_index = random.randint(0, len(themes) - 1)
                self.themes.append(themes[theme_index])
                themes.remove(themes[theme_index])
        else:
            self.themes = ya_gpt.generate_themes(self.round_limit)

        image_nums = list()

        if self.ai:
            last_image_number = common.last_ai_image_num
        else:
            last_image_number = common.last_image_num

        for i in range(0, last_image_number + 1):
            image_nums.append(i)

        for player in self.players:
            self.scoreboard[player] = 0
            self.last_used_card_index[player] = 5
            self.player_images[player] = list()

            for i in range(6 + self.round_limit):
                image_index = random.randint(0, len(image_nums) - 1)
                self.player_images[player].append(str(image_nums[image_index]))
                image_nums.remove(image_nums[image_index])

    async def next_round(self):

        self.answer.clear()
        self.vote.clear()
        self.user_id_to_answer_order.clear()
        self.user_index_to_picture_number.clear()
        self.picture_number_to_user_index.clear()
        self.picture_number_to_user_index.append(-1)

        for i in range(len(self.players)):
            self.user_index_to_picture_number.append(i + 1)
            self.picture_number_to_user_index.append(i)
        random.shuffle(self.user_index_to_picture_number)

        for i in range(len(self.user_index_to_picture_number)):
            self.picture_number_to_user_index[self.user_index_to_picture_number[i]] = i

        self.round += 1

        for player in self.players:

            keyboard = kb_client_game if player != self.host else kb_host_game
            await tg_utils.send_message_kb(player, replies.ROUND.format(cur=self.round, limit=self.round_limit),
                                           keyboard)

            image_names = list()
            for image_index in range(6):
                image_names.append(self.player_images[player][image_index])

            await tg_utils.send_images(user=player,
                                       caption=replies.THEME.format(theme=self.themes[self.round - 1]),
                                       image_names=image_names, ai=self.ai)

            common.action[player] = "раунд"

    async def end_game(self):

        winner_score = -1
        winners = 0
        for player in self.players:
            if self.scoreboard[player] > winner_score:
                winner_score = self.scoreboard[player]
                winners = [player]
            elif self.scoreboard[player] == winner_score:
                winners.append(player)

        winner_list_message = ""
        for winner in winners:
            winner_list_message += common.user_id_to_name[winner] + " "
        winner_list_message = winner_list_message.removesuffix(" ")

        for player in self.players:
            keyboard = kb_client if player != self.host else kb_host

            winner_placeholder = replies.WINNER
            if len(winners) > 1:
                winner_placeholder = replies.WINNERS

            await tg_utils.send_message_kb(player, replies.GAME_IS_OVER + "\n\n" +
                                           winner_placeholder.format(name=winner_list_message), keyboard)

    async def end_round(self):

        scoreboard_message = replies.SCOREBOARD_TITLE
        for player in self.players:
            scoreboard_message += "\n"
            scoreboard_message += common.user_id_to_name[player] + ": " + str(self.scoreboard[player])
        scoreboard_message += "\n\n" + replies.NEXT_ROUND_IN.format(time=5)

        await tg_utils.send_group_message(self.players, scoreboard_message)

        for player in self.players:
            common.action[player] = ""

            self.last_used_card_index[player] += 1
            self.player_images[player][int(self.answer[player]) - 1] = \
                self.player_images[player][self.last_used_card_index[player]]

        if self.round == self.round_limit:
            await self.end_game()
            return

        self.is_break = True
        time.sleep(2)
        self.is_break = False
        await self.next_round()

    async def voting(self):

        image_names = [0] * len(self.players)
        user_index = 0
        for player in self.players:
            image_names[self.user_index_to_picture_number[user_index] - 1] = \
                self.player_images[player][int(self.answer[player]) - 1]
            user_index += 1

        for player in self.players:
            common.action[player] = "vote"

            await tg_utils.send_images(user=player,
                                       image_names=image_names,
                                       caption=replies.VOTING_STAGE.format(cur=self.round, limit=self.round_limit) +
                                               "\n\n" + replies.THEME.format(theme=self.themes[self.round - 1]), ai=self.ai)

    async def set_vote(self, player, vote):

        await self.send_to_players(replies.PLAYER_HAS_VOTED.format(name=common.user_id_to_name[player]))
        self.vote[player] = vote
        self.scoreboard[self.players[self.picture_number_to_user_index[int(vote)]]] += \
            len(self.players) - self.user_id_to_answer_order[
                self.players[self.picture_number_to_user_index[int(vote)]]] + 1

        if len(self.vote) == len(self.players) and not self.vote_finished.keys().__contains__(self.round):
            self.vote_finished[self.round] = True
            await tg_utils.send_group_message(self.players, replies.VOTE_HAS_ENDED)
            await self.end_round()

    async def start(self):

        await self.prepare_game()

        self.is_started = True

        if self.ai:
            game_mode = "ИИ"
        else:
            game_mode = "Классический"

        for player in self.players:
            await tg_utils.send_message(player, replies.THE_GAME_HAS_BEEN_STARTED.format(time=5) + "\n\n" +
                                        replies.OPTIONS.format(game_mode=game_mode, round_limit=self.round_limit,
                                                               players_count=len(self.players)))

        await self.prepare_game()

        self.is_break = True
        time.sleep(2)
        self.is_break = False
        await self.next_round()

    async def set_answer(self, player, answer):

        await self.send_to_players(replies.PLAYER_SET_AN_ANSWER.format(name=common.user_id_to_name[player]))
        self.user_id_to_answer_order[player] = len(self.user_id_to_answer_order) + 1
        self.answer[player] = answer

        buttons = list()
        buttons_count = 0
        for i in range((len(self.players) - 1) // 3 + 1):
            buttons_row = list()
            for j in range(3):
                if buttons_count < len(self.players):
                    buttons_count += 1
                    buttons_row.append(KeyboardButton(text=str(buttons_count)))
            buttons.append(buttons_row)

        host_buttons = buttons.copy()
        host_buttons.append([KeyboardButton(text="Выйти и завершить игру")])
        host_keyboard = ReplyKeyboardMarkup(keyboard=host_buttons, resize_keyboard=True)

        client_buttons = buttons.copy()
        client_buttons.append([KeyboardButton(text="Выйти из игры")])
        client_keyboard = ReplyKeyboardMarkup(keyboard=client_buttons, resize_keyboard=True)

        if len(self.answer) == len(self.players) and not self.round_finished.keys().__contains__(self.round):
            self.round_finished[self.round] = True

            for player in self.players:

                if self.host == player:
                    await tg_utils.send_message_kb(message=replies.ROUND_HAS_ENDED,
                                                   user_id=player,
                                                   keyboard=host_keyboard)
                else:
                    await tg_utils.send_message_kb(message=replies.ROUND_HAS_ENDED,
                                                   user_id=player,
                                                   keyboard=client_keyboard)
            await self.voting()
