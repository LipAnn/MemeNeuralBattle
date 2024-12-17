import common
import default_menu
import replies
import tg_utils

games = list()


class Game:

    def __init__(self, code, host, limit_players):
        self.code = code
        self.host = host
        self.limit_players = limit_players
        self.players = list()

        self.players.append(host)
        common.host_to_game_code[host] = code
        common.game_code_to_host_dict[code] = host
        common.code_to_game[code] = self
        common.used_codes.append(self.code)

        games.append(self)

    async def join(self, player):

        for current_player in self.players:
            await tg_utils.send_message(current_player, replies.PLAYER_JOINED_TO_HOST_MESSAGE
                                        .format(name=common.user_id_to_name[player]))
            await tg_utils.send_message(current_player, replies.PLAYER_COUNT
                                        .format(cur=len(self.players) + 1, limit=self.limit_players))

        self.players.append(player)

    async def leave(self, player):
        self.players.remove(player)

        for current_player in self.players:
            await tg_utils.send_message(current_player, replies.PLAYER_LEFT_THE_GAME
                                        .format(name=common.user_id_to_name[player]))
            await tg_utils.send_message_kb(current_player, replies.PLAYER_COUNT
                                           .format(cur=len(self.players), limit=self.limit_players),
                                           reply_markup=default_menu.kb_default)

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
