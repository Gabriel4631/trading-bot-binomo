"""Launcher script for the Binomo demo bot."""

from .interfaz import TradingInterface


def main() -> None:
    app = TradingInterface()
    app.mainloop()


if __name__ == "__main__":
    main()
