import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv

# Load variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "একটু সমস্যা হয়েছে, পরে চেষ্টা করো।")

print("🤖 Bot is running...")
import time

while True:
    try:
        print("🤖 Bot is attempting to poll...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Connection error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
