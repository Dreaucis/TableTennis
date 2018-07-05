class RuleError(Exception):
    def __init__(self, rank_1, rank_2):
        self.rank_1 = rank_1
        self.rank_2 = rank_2
