from strategy import Strategy
from config import *

class MeanStrategy(Strategy):
    def __init__(
            self,
            entry_z=ENTRY_Z,
            exit_z=EXIT_Z):

        self.entry_z=entry_z
        self.exit_z=exit_z
        self.position=False



    def next(self,row):
        z=row["zscore"]
        if not self.position:
            if z <= self.entry_z:
                self.position=True
                return "BUY"
        else:
            if z >= self.exit_z:
                self.position=False
                return "SELL"
        return "HOLD"