import os
import telebot
import google.generativeai as genai
from dotenv import load_dotenv
import time

# ভেরিয়েবল লোড করা
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# জেমিনাই কনফিগার করা
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        # জেমিনাই থেকে উত্তর তৈরি করা
        response = model.generate_content(message.text)
        
        # যদি জেমিনাই উত্তর দেয়, তবে সেটি টেলিগ্রামে পাঠানো
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "জেমিনাই থেকে কোনো উত্তর পাওয়া যায়নি।")
            
    except Exception as e:
        # আসল সমস্যাটি কী তা দেখার জন্য প্রিন্ট করা
        error_message = str(e)
        print(f"❌ Gemini Error: {error_message}")
        
        # ব্যবহারকারীকে একটু ডিটেইল মেসেজ দেওয়া যাতে আপনি বুঝতে পারেন কী সমস্যা
        if "API_KEY_INVALID" in error_message:
            bot.reply_to(message, "আপনার Gemini API Key-টি ভুল। ঠিক করে আবার বসান।")
        elif "quota" in error_message.lower():
            bot.reply_to(message, "আপনার ফ্রি লিমিট শেষ হয়ে গেছে, কিছুক্ষণ পর চেষ্টা করুন।")
        else:
            bot.reply_to(message, f"সমস্যা: {error_message[:50]}...")

print("🤖 Bot is starting...")

# বটের পোলিং লুপ (কানেকশন এরর সামলানোর জন্য)
while True:
    try:
        print("🤖 Bot is attempting to poll...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"❌ Connection error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
