"""Representação de uma oferta e formatação da mensagem para o Telegram."""
from dataclasses import dataclass, asdict
from typing import Optional

# Emoji e hashtag de cada fonte de afiliado suportada.
SOURCES = {
    "amazon": {"label": "Amazon", "emoji": "🛒", "hashtag": "#Amazon"},
    "kabum": {"label": "KaBum", "emoji": "🖥️", "hashtag": "#KaBum"},
    "magalu": {"label": "Magazine Luiza", "emoji": "🛍️", "hashtag": "#Magalu"},
    "shopee": {"label": "Shopee", "emoji": "🧡", "hashtag": "#Shopee"},
}

CATEGORY_HASHTAGS = {
    "notebook": "#Notebook",
    "placa_de_video": "#PlacaDeVideo",
    "processador": "#Processador",
    "monitor": "#Monitor",
    "periferico": "#Periferico",
    "armazenamento": "#SSD",
    "componente": "#Hardware",
    "acessorio": "#Acessorio",
}


@dataclass
class Deal:
    id: str
    title: str
    category: str
    source: str
    price: float
    affiliate_link: str
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    posted: bool = False

    @property
    def discount_pct(self) -> Optional[int]:
        if not self.original_price or self.original_price <= self.price:
            return None
        return round((1 - self.price / self.original_price) * 100)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Deal":
        return Deal(**data)

    def format_price(self, value: float) -> str:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def build_message(self) -> str:
        source_info = SOURCES.get(self.source, {"label": self.source, "emoji": "🔗", "hashtag": ""})
        category_tag = CATEGORY_HASHTAGS.get(self.category, "")

        lines = [f"{source_info['emoji']} *{self.title}*", ""]

        if self.discount_pct:
            lines.append(f"~{self.format_price(self.original_price)}~ 👉 *{self.format_price(self.price)}*")
            lines.append(f"🔥 *{self.discount_pct}% OFF*")
        else:
            lines.append(f"💰 *{self.format_price(self.price)}*")

        lines.append("")
        lines.append(f"🔗 [Ver oferta]({self.affiliate_link})")
        lines.append("")

        tags = " ".join(t for t in [source_info["hashtag"], category_tag] if t)
        if tags:
            lines.append(tags)

        return "\n".join(lines)
