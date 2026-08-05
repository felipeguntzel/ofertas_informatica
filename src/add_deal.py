"""Adiciona uma nova oferta a data/deals.json de forma interativa.

Uso:
    python -m src.add_deal
"""
import json
import uuid
from pathlib import Path

from src.deal import CATEGORY_HASHTAGS, SOURCES, Deal

DEALS_PATH = Path(__file__).resolve().parent.parent / "data" / "deals.json"


def ask(prompt: str, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value


def ask_float(prompt: str, required: bool = True) -> float | None:
    raw = ask(prompt, required=required)
    return float(raw.replace(",", ".")) if raw else None


def main() -> None:
    print("Fontes disponíveis:", ", ".join(SOURCES.keys()))
    print("Categorias sugeridas:", ", ".join(CATEGORY_HASHTAGS.keys()))
    print()

    deal = Deal(
        id=str(uuid.uuid4())[:8],
        title=ask("Título do produto: "),
        category=ask("Categoria: "),
        source=ask("Fonte (amazon/kabum/magalu/shopee): "),
        price=ask_float("Preço atual (ex: 449.90): "),
        original_price=ask_float("Preço original (opcional, enter p/ pular): ", required=False),
        affiliate_link=ask("Link de afiliado: "),
        image_url=ask("URL da imagem (opcional, enter p/ pular): ", required=False) or None,
    )

    deals = []
    if DEALS_PATH.exists():
        with open(DEALS_PATH, encoding="utf-8") as f:
            deals = json.load(f)

    deals.append(deal.to_dict())

    with open(DEALS_PATH, "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Oferta '{deal.title}' adicionada! Rode 'python -m src.post_deals' para publicar.")


if __name__ == "__main__":
    main()
