# mercado_livre — Canal de Ofertas de Informática

Estrutura para divulgar ofertas de informática/computação em um canal do
Telegram, com links de afiliado de múltiplas fontes (Amazon, KaBum, Magazine
Luiza, Shopee).

## Como funciona

1. Você cadastra ofertas em `data/deals.json` (manualmente ou com o script
   `add_deal.py`).
2. O script `post_deals.py` lê as ofertas ainda não publicadas e posta cada
   uma no canal do Telegram, já formatada com preço, desconto e link de
   afiliado.
3. Ofertas já publicadas ficam marcadas (`"posted": true`) e não são
   reenviadas.

## 1. Criar o bot e o canal no Telegram

1. Abra uma conversa com **[@BotFather](https://t.me/BotFather)** no Telegram.
2. Envie `/newbot` e siga as instruções (nome e username do bot).
3. Guarde o **token** que o BotFather te enviar.
4. Crie um canal público (ex: `@ofertas_info_tech`) ou privado.
5. Adicione o bot como **administrador** do canal (permissão de postar
   mensagens).
6. Se o canal for público, o `TELEGRAM_CHANNEL_ID` é `@nome_do_canal`.
   Se for privado, veja como pegar o ID numérico
   [aqui](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id).

## 2. Configurar o projeto

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env com o token do bot e o ID do canal
```

## 3. Adicionar uma oferta

```bash
python -m src.add_deal
```

Ou edite `data/deals.json` diretamente seguindo o formato:

```json
{
  "id": "identificador-unico",
  "title": "Nome do produto",
  "category": "notebook",
  "source": "amazon",
  "price": 2999.00,
  "original_price": 3499.00,
  "affiliate_link": "https://seu-link-de-afiliado",
  "image_url": "https://url-da-imagem.jpg",
  "posted": false
}
```

Fontes suportadas: `amazon`, `kabum`, `magalu`, `shopee`.
Categorias sugeridas: `notebook`, `placa_de_video`, `processador`,
`monitor`, `periferico`, `armazenamento`, `componente`, `acessorio`.

## 4. Publicar as ofertas pendentes

```bash
python -m src.post_deals
```

## Onde conseguir os links de afiliado

- **Amazon Associates**: [associados.amazon.com.br](https://associados.amazon.com.br)
- **KaBum (via Awin)**: cadastro na [Awin](https://www.awin.com/br) e solicitação
  do programa KaBum
- **Magazine Luiza (Parceiro Magalu)**: cadastro direto no site do Magalu
- **Shopee**: programa de afiliados Shopee

## Próximos passos possíveis

- Agendar `post_deals.py` para rodar automaticamente (cron, GitHub Actions).
- Buscar ofertas automaticamente por categoria em cada fonte (APIs oficiais
  quando disponíveis, respeitando os termos de uso de cada loja).
- Replicar o mesmo conteúdo em outros canais (Instagram, WhatsApp).
