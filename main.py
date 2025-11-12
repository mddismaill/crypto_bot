import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
PRIVATE_CHANNEL_LINK = os.getenv("PRIVATE_CHANNEL_LINK")
WEBHOOK_URL = f"https://crypto-bot-1-5xna.onrender.com/{BOT_TOKEN}"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 🔹 Создание счёта в CryptoBot
def create_invoice(amount, user_id):
    url = "https://pay.crypt.bot/api/createInvoice"
    payload = {
        "asset": "USDT",
        "amount": amount,
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
    response = requests.post(url, json=payload, headers=headers).json()
    return response["result"]["pay_url"]

# 🔸 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Чтобы получить доступ к закрытому каналу, пожалуйста, ознакомьтесь с нашей офертой и политикой конфиденциальности."
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💳 Оплатить 5 USDT", callback_data="pay"))
    bot.send_message(
        message.chat.id,
        "Стоимость: 5 USDT",
        reply_markup=markup
    )

# 🔸 Обработка оплаты
@bot.callback_query_handler(func=lambda call: call.data == "pay")
def pay_handler(call):
    url = create_invoice(5, call.from_user.id)
    bot.send_message(call.message.chat.id, f"👉 Оплатите по ссылке:\n{url}")

# 🔹 Flask webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Сбрасываем старый webhook и ставим новый
    bot.remove_webhook()
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

    # Запуск Flask
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

