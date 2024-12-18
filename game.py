import common
import default_menu
import replies
import tg_utils
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
        self.round_limit = 10
        self.answer = dict()
        self.finished = dict()

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
        self.themes = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}

    async def next_round(self):

        self.answer.clear()
        self.round += 1

        for player in self.players:
            common.action[player] = "раунд"

            keyboard = kb_client_game if player != self.host else kb_host_game
            await tg_utils.send_message_kb(player, replies.ROUND.format(cur=self.round, limit=self.round_limit),
                                           keyboard)

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

        if len(self.answer) == len(self.players) and not self.finished.keys().__contains__(self.round):
            self.finished[self.round] = True
            await self.end_round()
