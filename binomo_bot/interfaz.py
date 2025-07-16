"""tkinter based GUI for the trading bot."""

import tkinter as tk
from tkinter import ttk

from .operaciones import Trader


class TradingInterface(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Binomo Demo Bot")
        self.configure(bg="#222222")
        self.geometry("800x500")

        self.trader = Trader()
        self.create_widgets()
        self.update_balance()

    def create_widgets(self) -> None:
        control_frame = tk.Frame(self, bg="#222222")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(control_frame, text="Initial Investment", fg="white", bg="#222222").pack(anchor="w")
        self.initial_entry = tk.Entry(control_frame)
        self.initial_entry.insert(0, "10000")
        self.initial_entry.pack(anchor="w")

        tk.Label(control_frame, text="Trade Time", fg="white", bg="#222222").pack(anchor="w", pady=(10, 0))
        self.time_combo = ttk.Combobox(control_frame, values=["30s", "1min", "2min"], width=10)
        self.time_combo.current(0)
        self.time_combo.pack(anchor="w")

        tk.Label(control_frame, text="Cycle Goal", fg="white", bg="#222222").pack(anchor="w", pady=(10, 0))
        self.cycle_entry = tk.Entry(control_frame)
        self.cycle_entry.insert(0, "200000")
        self.cycle_entry.pack(anchor="w")

        tk.Label(control_frame, text="Total Goal", fg="white", bg="#222222").pack(anchor="w", pady=(10, 0))
        self.total_entry = tk.Entry(control_frame)
        self.total_entry.insert(0, "1000000")
        self.total_entry.pack(anchor="w")

        self.start_button = tk.Button(control_frame, text="Start", command=self.start_trading)
        self.start_button.pack(pady=(20, 0), fill="x")

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_trading)
        self.stop_button.pack(fill="x")

        log_frame = tk.Frame(self, bg="#333333")
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.balance_var = tk.StringVar()
        tk.Label(log_frame, textvariable=self.balance_var, fg="cyan", bg="#333333", font=("Arial", 14, "bold")).pack()

        self.history_text = tk.Text(log_frame, state="disabled", bg="#111111", fg="white")
        self.history_text.pack(fill=tk.BOTH, expand=True)

    def update_balance(self) -> None:
        self.balance_var.set(f"Balance: ${self.trader.balance:.2f}")
        self.after(1000, self.update_balance)

    def start_trading(self) -> None:
        self.trader.balance = float(self.initial_entry.get())
        self.trader.trade_time = self.time_combo.get()
        self.trader.cycle_goal = float(self.cycle_entry.get())
        self.trader.total_goal = float(self.total_entry.get())
        self.after(1000, self.run_trade)

    def run_trade(self) -> None:
        self.trader.trade()
        item = self.trader.history[-1]
        self.history_text.configure(state="normal")
        self.history_text.insert(tk.END, f"{item.action} {item.amount:.2f} -> {item.result}\n")
        self.history_text.see(tk.END)
        self.history_text.configure(state="disabled")
        self.after(1000, self.run_trade)

    def stop_trading(self) -> None:
        self.after_cancel(self.run_trade)

