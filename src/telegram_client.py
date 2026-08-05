"""Cliente mínimo para a Bot API do Telegram (sem dependências pesadas)."""
import requests

API_BASE = "https://api.telegram.org/bot{token}"


class TelegramClient:
    def __init__(self, bot_token: str, channel_id: str):
        if not bot_token or not channel_id:
            raise ValueError("TELEGRAM_BOT_TOKEN e TELEGRAM_CHANNEL_ID são obrigatórios")
        self.bot_token = bot_token
        self.channel_id = channel_id

    def _url(self, method: str) -> str:
        return f"{API_BASE.format(token=self.bot_token)}/{method}"

    def send_message(self, text: str, disable_preview: bool = False) -> dict:
        resp = requests.post(
            self._url("sendMessage"),
            data={
                "chat_id": self.channel_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": disable_preview,
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    def send_photo(self, photo_url: str, caption: str) -> dict:
        resp = requests.post(
            self._url("sendPhoto"),
            data={
                "chat_id": self.channel_id,
                "photo": photo_url,
                "caption": caption,
                "parse_mode": "Markdown",
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
