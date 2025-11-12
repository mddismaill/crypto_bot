import telebot
import requests

# 🔑 Токены
BOT_TOKEN = "8260133446:AAEbZFM6jVanpbxs8fXforL_3Eidko_a-ok"
CRYPTOBOT_TOKEN = "486679:AAV18bi9lLsoASFedRmuurht4il1C7eSAPK"
PRIVATE_CHANNEL_LINK = "https://t.me/Daily_Combo_Secret_Code"

bot = telebot.TeleBot(BOT_TOKEN)

# 💰 Создание счёта
def create_invoice(amount, user_id):
    url = "https://pay.crypt.bot/api/createInvoice"
    payload = {
        "asset": "USDT",     # Валюта (можно BTC, TON и т.д.)
        "amount": amount,    # Сумма
        "description": "Доступ к курсу",
        "hidden_message": "После оплаты получите доступ к закрытому каналу.",
        "paid_btn_name": "openChannel",
        "paid_btn_url": PRIVATE_CHANNEL_LINK,
        "allow_comments": False,
        "allow_anonymous": True
    }
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_TOKEN,
        "Content-Type": "application/json"
    }
    r = requests.post(url, json=payload, headers=headers).json()
    return r["result"]["pay_url"]

# 🚀 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Здесь можно купить доступ к закрытому каналу.\n\n"
        "Стоимость: 5 USDT\n"
        "Нажми кнопку ниже, чтобы оплатить.",
        reply_markup=telebot.types.InlineKeyboardMarkup().add(
            telebot.types.InlineKeyboardButton("💳 Оплатить 5 USDT", callback_data="pay")
        )
    )

# 💸 Обработка кнопки оплаты
@bot.callback_query_handler(func=lambda call: call.data == "pay")
def pay_handler(call):
    invoice_url = create_invoice(amount=5, user_id=call.from_user.id)
    bot.send_message(call.message.chat.id, f"Перейдите для оплаты:\n{invoice_url}")

bot.polling(none_stop=True)
