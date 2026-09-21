import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config={'system_instruction': SYSTEM_INSTRUCTION}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء المعالجة: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Agent is starting...")
    app.run_polling()
