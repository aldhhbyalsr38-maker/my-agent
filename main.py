import os
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# --- 1. خادم ويب مصغر لإبقاء الخدمة مجانية على Render ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Agent is running live 24/7!"

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- 2. إعدادات بوت التلغرام و Gemini ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
أنت وكيل ذكاء اصطناعي مستقل متناغم لخبير التجارة الإلكترونية والدروب شيبينغ.
تتحدث باللغة العربية بأسلوب عملي، احترافي ومشجع.
تساعد صاحب المتجر على اختيار المنتجات المربحة، وضع استراتيجيات تسويق عبر TikTok وReels، وأتمتة الأفكار خطوة بخطوة.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # تعديل اسم الموديل إلى الإصدار الصحيح والمطلوب
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config={'system_instruction': SYSTEM_INSTRUCTION}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء المعالجة: {e}")

if __name__ == '__main__':
    # تشغيل خادم الويب
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # تشغيل البوت مع إنهاء أي اتصالات معلقة لحل مشكلة Conflict
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Agent is starting...")
    app.run_polling(drop_pending_updates=True)
