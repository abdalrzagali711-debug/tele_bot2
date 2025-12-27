import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from rembg import remove
from io import BytesIO

# قراءة التوكن من متغير البيئة
TOKEN = os.getenv("TOKEN")

# إنشاء التطبيق
app = ApplicationBuilder().token(TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "البوت شغال 👌\nأرسل أي صورة ليتم إزالة الخلفية."
    )

# معالجة الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = BytesIO()
        await photo_file.download(out=photo_bytes)
        photo_bytes.seek(0)

        # إزالة الخلفية
        output_bytes = remove(photo_bytes.read())
        await update.message.reply_photo(photo=BytesIO(output_bytes))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

# إضافة المعالجات
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# تشغيل البوت
print("تشغيل البوت…")
app.run_polling()
