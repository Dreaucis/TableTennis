import sqlite3
import numpy as np
from Connector import Connector

class Game(Connector):
    # Initialization
    def __init__(self, id_player_1,id_player_2,score_player_1,score_player_2,db_cursor):
        super.__init__(db_cursor)
        self.dict = {'id': self.getNextId(),
                      'id_player_1': id_player_1,
                      'id_player_2': id_player_2,
                      'score_player_1': score_player_1,
                      'score_player_2':score_player_2
                     }


    # Methods
    def getNextId(self):
        return self.db_cursor.execute(""" SELECT MAX(id) + 1 FROM games """).fetchone()[0]

    def addResults(self):
        scores = [self.dict['score_player_1'], self.dict['score_player_2']]
        # If any score is over 11 the difference must be less than 3 in score.
        # Any score with max score 11 is also valid as long as both scores are not 11.
        if (any([x > 11 for x in scores]) and (np.diff[scores] < 3)) \
                or (np.max(scores) == 11 and not all([x == 11 for x in scores])):
            self.db_cursor.execute(""" 
            INSERT INTO games(id,id_player_1,id_player_2,score_player_1,score_player_2)
            VALUES(:id,:id_player_1,:id_player_2,:score_player_1,:score_player_2) 
            """, self.dict)
        else:
            print('Invalid score')
