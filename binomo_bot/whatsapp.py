"""Simulated WhatsApp notification module."""

from datetime import datetime


def send_message(text: str) -> None:
    """Simulate sending a WhatsApp message by printing to stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WhatsApp {timestamp}] {text}")
