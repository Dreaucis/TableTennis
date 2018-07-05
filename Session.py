from Game import Game
from Ladder import Ladder
from Player import Player
from RuleError import RuleError
import sqlite3


class Session:
    def __init__(self):
        """
        Connects to the sqlite table_tennis database
        """
        self.db = sqlite3.connect('table_tennis.db')

    def geIdsAndNames(self):
        """
        Gets the id and name of all players in the players table.
        :return: returns a list of tuples of names (string) and id (int)
        """
        return self.db.execute(""" SELECT id,name FROM players """).fetchall()

    def addResult(self, player_id_1, player_id_2, score_1, score_2):
        """
        Adds results of a game to the games tables. Swaps player ranks in the ladder table if appropriate.
        :param player_id_1: id of the first player
        :param player_id_2: id of the second player
        :param score_1: score of the first player
        :param score_2: score of the second player
        :type player_id_1: int
        :type player_id_2: int
        :type score_1: int
        :type score_2: int
        """
        try:
            Ladder(self.db.cursor()).addResults(player_id_1, player_id_2, score_1, score_2)
            Game([player_id_1, player_id_2], [score_1, score_2], self.db.cursor()).addResults()
            self.db.commit()
        except RuleError as e:
            print('Player ranks {0} and {1} are too far apart. No results were added.'.format(e.rank_1, e.rank_2))

    def addPlayer(self, name):
        """
        Adds a player to the ladder and player tables.
        :param name: name of player
        :type name: str
        """
        try:
            Player(self.db.cursor()).addPlayer(name)
            Ladder(self.db.cursor()).addPlayer(name)
            self.db.commit()
        except ValueError:
            print('Could not add player. Name is taken.')

    def removePlayer(self, name_or_id):
        """
        Removes a player from the ladder and player tables. Does not remove player form the games table.
        :param name_or_id: name or id of player.
        :type name_or_id: str, int
        """
        try:
            Ladder(self.db.cursor()).removePlayer(name_or_id)
            Player(self.db.cursor()).removePlayer(name_or_id)
            db.commit()
        except ValueError:
            print('Could not remove player. Player name or id is not valid')



