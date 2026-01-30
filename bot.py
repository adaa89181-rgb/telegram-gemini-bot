from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not TELEGRAM_TOKEN or not GOOGLE_API_KEY:
    raise ValueError("❌ Token বা API key পাওয়া যায়নি")
import logging
import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

import google.generativeai as genai

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ Token বা API key পাওয়া যায়নি")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    try:
        # যদি model.generate_content() ব্লকিং হয় — সেটা event-loop ব্���ক করলে 안된다।
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(user_text))

        # response থেকে টেক্সট বের করার রবারস্ট লজিক
        text = None
        if hasattr(response, "text") and response.text:
            text = response.text
        elif hasattr(response, "candidates") and response.candidates:
            cand = response.candidates[0]
            text = getattr(cand, "content", None) or getattr(cand, "output", None) or str(cand)
        else:
            # fallback: পুরো রেসপন্স স্ট্রিং আকারে পাঠান
            text = str(response)

        await update.message.reply_text(text)
    except Exception as e:
        logger.exception("Generative API error:")
        await update.message.reply_text("⚠️ এখন সমস্যা হচ্ছে, পরে চেষ্টা করো")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    logger.info("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()EXT impoEXT
