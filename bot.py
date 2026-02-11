import telebot
import random
import json
import os
from datetime import datetime

# ====== CẤU HÌNH ======
TOKEN = "8478101205:AAEYC7-eYf1XDyWxynvS-Z-JCvU59WOr1Tw"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"
START_BALANCE = 1000

# ====== LOAD / SAVE DATA ======
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

users = load_data()

def get_user(uid):
    uid = str(uid)
    if uid not in users:
        users[uid] = {
            "balance": START_BALANCE,
            "last_daily": ""
        }
        save_data(users)
    return users[uid]

# ====== START ======
@bot.message_handler(commands=["start"])
def start(message):
    user = get_user(message.from_user.id)
    bot.reply_to(
        message,
        "🎮 <b>MarketModVN Game Bot</b>\n\n"
        "💰 Số dư khởi đầu: <b>1000</b>\n\n"
        "📜 Lệnh:\n"
        "/balance – xem số dư\n"
        "/daily – nhận quà ngày\n"
        "/taixiu – chơi tài xỉu\n"
        "/coin – tung xu\n"
        "/guess – đoán số",
        parse_mode="HTML"
    )

# ====== BALANCE ======
@bot.message_handler(commands=["balance"])
def balance(message):
    user = get_user(message.from_user.id)
    bot.reply_to(message, f"💰 Số dư hiện tại: <b>{user['balance']}</b>", parse_mode="HTML")

# ====== DAILY ======
@bot.message_handler(commands=["daily"])
def daily(message):
    user = get_user(message.from_user.id)
    today = datetime.now().strftime("%Y-%m-%d")

    if user["last_daily"] == today:
        bot.reply_to(message, "⏳ Bạn đã nhận quà hôm nay rồi!")
        return

    reward = random.randint(200, 500)
    user["balance"] += reward
    user["last_daily"] = today
    save_data(users)

    bot.reply_to(message, f"🎁 Bạn nhận được <b>{reward}</b> coin!", parse_mode="HTML")

# ====== TÀI XỈU ======
@bot.message_handler(commands=["taixiu"])
def taixiu(message):
    user = get_user(message.from_user.id)

    dice = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
    result = "TÀI" if dice >= 11 else "XỈU"

    win = random.choice([True, False])
    if win:
        user["balance"] += 200
        text = f"🎲 Kết quả: {dice} ({result})\n✅ Bạn thắng +200"
    else:
        user["balance"] -= 150
        text = f"🎲 Kết quả: {dice} ({result})\n❌ Bạn thua -150"

    save_data(users)
    bot.reply_to(message, text)

# ====== COIN FLIP ======
@bot.message_handler(commands=["coin"])
def coin(message):
    user = get_user(message.from_user.id)
    side = random.choice(["🪙 Ngửa", "🪙 Sấp"])

    if side == "🪙 Ngửa":
        user["balance"] += 100
        text = f"{side}\n✅ Thắng +100"
    else:
        user["balance"] -= 50
        text = f"{side}\n❌ Thua -50"

    save_data(users)
    bot.reply_to(message, text)

# ====== GUESS NUMBER ======
@bot.message_handler(commands=["guess"])
def guess(message):
    num = random.randint(1,5)
    bot.reply_to(
        message,
        f"🎯 Số bí mật là: <b>{num}</b>\n(+/- coin ngẫu nhiên)",
        parse_mode="HTML"
    )

# ====== FALLBACK ======
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(message, "❓ Không hiểu lệnh. Gõ /start để xem menu.")

print("🤖 Bot đang chạy...")
bot.infinity_polling()
