from dataclasses import dataclass


@dataclass
class Trade:
    entry_time: int
    exit_time: int
    entry_spread: float
    exit_spread: float
    direction: str
    pnl: float
    fee: float
    hold_seconds: int
    pnl_after_fee: float