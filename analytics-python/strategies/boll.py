from strategy import Strategy


class BollStrategy(Strategy):

    def __init__(self):
        self.position=False


    def next(self,row):
        price=row["spread"]
        ma=row["ma20"]
        std=row["std20"]
        upper=ma+2*std
        lower=ma-2*std

        if not self.position:
            if price < lower:
                self.position=True
                return "BUY"

        else:
            if price >= ma:
                self.position=False
                return "SELL"
            
        return "HOLD"