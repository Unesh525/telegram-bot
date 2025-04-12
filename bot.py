import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN env variable से लिया जाएगा
TOKEN = os.environ["TOKEN"]

# Image URL (तेरा QR या कोई प्रमोशन इमेज)
IMAGE_URL = "qr.png"  # 👈 यहाँ अपनी इमेज का लिंक डाल

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "<b>Kindly Pay ₹99 And Submit Screenshot</b>\n\n"
        "1. Phone Pe\n"
        "2. Paytm\n"
        "3. G Pay\n"
        "4. Spotify Premium\n\n"
        
    )

    # इमेज के साथ टेक्स्ट भेजो (caption के रूप में)
    await update.message.reply_photo(photo=IMAGE_URL, caption=message, parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
