"""Posta no canal do Telegram todas as ofertas pendentes em data/deals.json.

Uso:
    python -m src.post_deals
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from src.deal import Deal
from src.telegram_client import TelegramClient

DEALS_PATH = Path(__file__).resolve().parent.parent / "data" / "deals.json"
DELAY_BETWEEN_POSTS_SECONDS = 3


def load_deals() -> list[Deal]:
    with open(DEALS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return [Deal.from_dict(d) for d in raw]


def save_deals(deals: list[Deal]) -> None:
    with open(DEALS_PATH, "w", encoding="utf-8") as f:
        json.dump([d.to_dict() for d in deals], f, ensure_ascii=False, indent=2)


def main() -> None:
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    client = TelegramClient(bot_token, channel_id)

    deals = load_deals()
    pending = [d for d in deals if not d.posted]

    if not pending:
        print("Nenhuma oferta pendente para postar.")
        return

    for deal in pending:
        message = deal.build_message()
        try:
            if deal.image_url:
                client.send_photo(deal.image_url, message)
            else:
                client.send_message(message)
            deal.posted = True
            print(f"✅ Postado: {deal.title}")
        except Exception as exc:
            print(f"❌ Falha ao postar '{deal.title}': {exc}", file=sys.stderr)

        time.sleep(DELAY_BETWEEN_POSTS_SECONDS)

    save_deals(deals)


if __name__ == "__main__":
    main()
