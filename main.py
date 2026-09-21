import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
أنت "وكيل ذكاء اصطناعي مستقل لخبير التجارة الإلكترونية والدروب شيبينغ".
تتحدث باللغة العربية، لديك رؤية ثاقبة واقتراحات مستمرة للتسويق، اختيار المنتجات، وإدارة المتاجر.
تساعد صاحب المتجر على أتمتة أعماله، تقديم استراتيجيات التسويق، وتوجيهه خطوة بخطوة.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء معالجة الطلب: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Agent is running...")
    app.run_polling()

