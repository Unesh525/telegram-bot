import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN env variable से लिया जाएगा
TOKEN = os.environ["TOKEN"]

# Image URL (तेरा QR या कोई प्रमोशन इमेज)
  # 👈 यहाँ अपनी इमेज का लिंक डाल

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        IMAGE_URL = "qr.png"
        "**Kindly Pay ₹99 And Submit UTR Number**\n\n"
        "1. Phone Pe\n"
        "2. Paytm\n"
        "3. G Pay\n"
        "4. Spotify Premium\n\n"
        "🎥 *Tutorial Video How to Buy From Bot:*\n"
        "[Click here to watch](https://t.me/phonepe_New/3)"
    )

    # टेक्स्ट भेजो (Markdown formatting)
    await update.message.reply_text(message, parse_mode="Markdown")

    # फिर इमेज भेजो
    await update.message.reply_photo(photo=IMAGE_URL)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
