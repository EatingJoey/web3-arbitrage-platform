from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def next(self, row):
        """
        输入行情数据
        返回:
        BUY
        SELL
        HOLD
        """
        pass