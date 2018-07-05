from Connector import Connector
from RuleError import RuleError


class Ladder(Connector):
    def __init__(self, db_cursor):
        super.__init__(db_cursor)

    def addPlayer(self, name):
        # Add player If the player name is not taken
        id_player = self.db_cursor.execute(""" SELECT id FROM players WHERE name = ? """, (name,)).fetchone()[0]
        rank = self.db_cursor.execute(""" SELECT COALESCE(MAX(rank),0) + 1 FROM ladder """).fetchone()[0]
        self.db_cursor.execute(""" INSERT INTO ladder(player_id,rank) VALUES(?,?) """, (id_player, rank))

    def removePlayer(self, name_or_id):
        if isinstance(name_or_id, str):
            name_or_id = \
            self.db_cursor.execute(""" SELECT id FROM players WHERE name = ? """, (name_or_id,)).fetchone()[0]
        self.db_cursor.execute(""" DELETE FROM ladder WHERE player_id = ? """, (name_or_id,))

        # TODO: This very much needs testing
        id_and_row_number = self.db_cursor.execute(""" 
        SELECT player_id, (SELECT COUNT(*) FROM ladder b WHERE a.rank > b.rank) as row_number FROM ladder a 
        """).fetchall()

        for pair in id_and_row_number:
            self.db_cursor.execute("""
            UPDATE ladder SET rank = (SELECT COUNT(*) FROM ladder b INNER JOIN ladder a ON b.player_id = a.player_id WHERE a.rank > b.rank))
            """,id_and_row_number)

    def addResults(self, id_player_1, id_player_2, score_player_1, score_player_2):
        rank_player_1 = self.db_cursor.execute(""" SELECT rank FROM ladder WHERE id = ? """, (id_player_1,))
        rank_player_2 = self.db_cursor.execute(""" SELECT rank FROM ladder WHERE id = ? """, (id_player_2,))
        # Swap ranks if:
        # - Player one has higher score AND lower rank
        # - OR Player two has higher score AND lower rank
        if (score_player_1 > score_player_2 and rank_player_1 < rank_player_2) \
                or (score_player_1 < score_player_2 and rank_player_1 > rank_player_2):
            self.db_cursor.execute(""" UPDATE ladder SET rank = ? WHERE id = ? """, (rank_player_2, id_player_1))
            self.db_cursor.execute(""" UPDATE ladder SET rank = ? WHERE id = ? """, (rank_player_1, id_player_2))

    def _isLegalMatch(self, rank_player_1, rank_player_2):
        if abs(rank_player_1 - rank_player_2) > 2:
            raise RuleError(rank_player_1, rank_player_2)

