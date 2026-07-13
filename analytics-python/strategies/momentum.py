from strategy import Strategy



class MomentumStrategy(Strategy):


    def __init__(self):
        self.position=False



    def next(self,row):
        ma20=row["ma20"]
        ma60=row["ma60"]
        spread=row["spread"]
        if not self.position:
            if ma20 > ma60:
                self.position=True
                return "BUY"
        else:
            if ma20 < ma60:
                self.position=False
                return "SELL"
        return "HOLD"