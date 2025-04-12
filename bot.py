import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, CallbackQueryHandler
)

# ENV से Token और Admin ID लो
TOKEN = os.environ["TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])  # Admin का Telegram user ID

# Image path
IMAGE_PATH = "qr.png"

# Files to send when approved
FILES_TO_SEND = ["GPay_1.0_enc_sign (1).apk", "Latest phonepe Gamerx24x7.apk", "Paytm_sign_d8803a30_enc_sign_@DARKSTUFF69.apk"]  # अपनी files डाल

# Store users' data for approval system
user_data = {}  # message_id: user_id mapping

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "<b>Kindly Pay ₹99 And Submit Screenshot</b>\n\n"
        "1. PhonePe\n"
        "2. Paytm\n"
        "3. GPay\n"
        "4. Spotify Premium\n\n"
        "📽️ <b>Tutorial Video:</b> <a href='https://t.me/phonepe_New/3'>Click here</a>"
    )
    await update.message.reply_photo(
        photo=IMAGE_PATH,
        caption=message,
        parse_mode="HTML"
    )

# जब यूज़र screenshot भेजे
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1]
    caption = f"🧾 Payment Screenshot from @{user.username or user.first_name} (ID: {user.id})"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user.id}")
        ]
    ])
    sent = await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption,
        reply_markup=keyboard
    )

    user_data[sent.message_id] = user.id

# जब Admin Approve/Reject दबाए
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Your payment has been *Approved!* Files are being sent...",
            parse_mode="Markdown"
        )
        for file_path in FILES_TO_SEND:
            if os.path.exists(file_path):
                await context.bot.send_document(chat_id=user_id, document=open(file_path, "rb"))
            else:
                await context.bot.send_message(chat_id=ADMIN_ID, text=f"⚠️ File not found: {file_path}")
        await query.edit_message_caption(caption="✅ Payment Approved.", reply_markup=None)

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ *Your payment has been Rejected!*\n"
                "🧾 *Reason: Payment screenshot is wrong.*"
            ),
            parse_mode="Markdown"
        )
        await query.edit_message_caption(caption="❌ Payment Rejected.", reply_markup=None)

    await query.answer()

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
