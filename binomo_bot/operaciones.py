"""Trading logic for demo purposes."""

from dataclasses import dataclass, field
import random
from typing import List

from .whatsapp import send_message


@dataclass
class TradeHistoryItem:
    action: str
    amount: float
    result: str


@dataclass
class Trader:
    balance: float = 10000.0
    cycle_goal: float = 200000.0
    total_goal: float = 1000000.0
    trade_time: str = "30s"
    history: List[TradeHistoryItem] = field(default_factory=list)

    def reset_cycle(self) -> None:
        self.balance = 10000.0

    def trade(self) -> None:
        if self.balance <= 0:
            self.reset_cycle()
            return

        prediction = random.choice(["HIGH", "LOW"])
        amount = self.balance
        # Simulate 80% chance of win for demo
        win = random.random() < 0.6
        if win:
            profit = amount * 0.8
            self.balance += profit
            result = "won"
        else:
            self.balance -= amount
            result = "lost"

        self.history.append(TradeHistoryItem(action=prediction, amount=amount, result=result))

        if self.balance >= self.cycle_goal:
            send_message("Cycle goal reached. Resetting balance to $10,000")
            self.reset_cycle()

        if self.balance >= self.total_goal:
            send_message("Total goal reached. Stopping bot.")
            raise SystemExit
