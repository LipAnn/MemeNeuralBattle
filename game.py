import random

import common
import default_menu
import replies
import tg_utils
from keyboard import kb_host_game, kb_client_game, kb_host, kb_client
import bisect

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
        self.round_limit = 10
        self.answer = dict()
        self.finished = dict()
        self.last_used_card_index = dict()

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

        for current_player in self.players:
            await tg_utils.send_message(current_player,
                                        replies.PLAYER_JOINED_TO_HOST_MESSAGE
                                        .format(name=common.user_id_to_name[player]) + "\n" +
                                        replies.PLAYER_COUNT
                                        .format(cur=len(self.players) + 1, limit=self.limit_players))

        self.players.append(player)

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

        with open("themes/themes.txt", encoding="UTF-8") as themes_file:
            themes = themes_file.readlines()
        for i in range(self.round_limit):
            theme_index = random.randint(0, len(themes) - 1)
            self.themes.append(themes[theme_index])
            themes.remove(themes[theme_index])

        image_nums = list()
        for i in range(0, common.last_image_num + 1):
            image_nums.append(i)

        for player in self.players:
            self.last_used_card_index[player] = 5
            self.player_images[player] = list()

            for i in range(6 + self.round_limit):
                image_index = random.randint(0, len(image_nums) - 1)
                self.player_images[player].append(str(image_nums[image_index]))
                image_nums.remove(image_nums[image_index])

    async def next_round(self):

        self.answer.clear()
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
                                       image_names=image_names)

            common.action[player] = "раунд"

    async def end_game(self):

        for player in self.players:
            keyboard = kb_client if player != self.host else kb_host

            await tg_utils.send_message_kb(player, replies.GAME_IS_OVER, keyboard)

    async def end_round(self):

        for player in self.players:
            common.action[player] = ""

            await tg_utils.send_message(player, replies.ROUND_HAS_ENDED.format(cur=self.round, limit=self.round_limit))

        if self.round == self.round_limit:
            await self.end_game()
            return

        await self.next_round()

    async def start(self):

        await self.prepare_game()

        self.is_started = True

        for player in self.players:
            await tg_utils.send_message(player, replies.THE_GAME_HAS_BEEN_STARTED)

        await self.next_round()

    async def set_answer(self, player, answer):

        await self.send_to_players(replies.PLAYER_SET_AN_ANSWER.format(name=common.user_id_to_name[player]))
        self.answer[player] = answer

        self.last_used_card_index[player] += 1
        self.player_images[player][int(answer) - 1] = self.player_images[player][self.last_used_card_index[player]]

        if len(self.answer) == len(self.players) and not self.finished.keys().__contains__(self.round):
            self.finished[self.round] = True
            await self.end_round()
