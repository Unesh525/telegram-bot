import os
from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN env variable से लिया जाएगा
TOKEN = os.environ["TOKEN"]

# Admin का Telegram User ID (तुम्हारा User ID)
ADMIN_USER_ID = "7850701411"  # Admin का Telegram ID यहां डालो

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

# जब यूजर स्क्रीनशॉट भेजे, तो उसे admin को भेजो
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # यूजर ने जो स्क्रीनशॉट भेजा है, उसे प्राप्त करना
    file = await update.message.photo[-1].get_file()

    # स्क्रीनशॉट का लिंक प्राप्त करें (डाउनलोड लिंक)
    file_url = file.file_path

    # Admin को स्क्रीनशॉट भेजो
    admin_message = f"New screenshot received!\n\nFile URL: {file_url}\n\nUser: {update.message.from_user.username}"
    await context.bot.send_message(chat_id=ADMIN_USER_ID, text=admin_message)

    # Admin को approval/rejection के ऑप्शन के साथ मैसेज भेजें
    buttons = [
        [
            ("Approve", "approve"),  # Approve बटन
            ("Reject", "reject")     # Reject बटन
        ]
    ]
    await context.bot.send_message(
        chat_id=ADMIN_USER_ID,
        text="Please approve or reject this payment screenshot:",
        reply_markup={"inline_keyboard": buttons}
    )

# Admin के द्वारा approve/reject की कार्रवाई को हैंडल करें
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action = query.data

    # Action के आधार पर जवाब भेजें
    if action == "approve":
        await query.answer("Payment Approved! 🎉")
        await query.message.reply_text("The payment screenshot has been approved.")
    elif action == "reject":
        await query.answer("Payment Rejected! 🚫")
        await query.message.reply_text("The payment screenshot has been rejected.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handler जोड़ें
    app.add_handler(CommandHandler("start", start))

    # स्क्रीनशॉट का हैंडलर जोड़ें
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    # बटन क्लिक पर handler जोड़ें
    app.add_handler(MessageHandler(filters.CallbackQuery, button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
