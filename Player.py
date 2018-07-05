from Connector import Connector


class Player(Connector):
    def __init__(self, db_cursor):
        super.__init__(db_cursor)

    # Methods
    def addPlayer(self, name):
        # Add player If the player name is not taken
        if not self.db_cursor.execute(""" SELECT * FROM players WHERE name = ? """, (name,)).fetchone():
            id_player = self.db_cursor.execute(""" SELECT COALESCE(MAX(id),0) + 1 FROM players """).fetchone()[0]
            self.db_cursor.execute(""" INSERT INTO players(id,name) VALUES(?,?) """, (id_player, name))
        else:
            raise ValueError

    def removePlayer(self, name_or_id):
        if isinstance(name_or_id,(str,int)):
            self.db_cursor.execute(""" DELETE FROM players WHERE id = ? OR name = ? """,(name_or_id,name_or_id))
        else:
            raise ValueError
