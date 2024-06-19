from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import time

# توکن API ربات شما
TOKEN = '7323769984:AAHqFqlljpTHVbt_CFHP5v2NYhGK54WDB7w'
PUBLIC_CHANNEL_USERNAME = '@future_surprise'
PRIVATE_CHANNEL_ID = 'YOUR_PRIVATE_CHANNEL_ID'  # ID کانال خصوصی شما
VIDEOS = {
    "video_link_1": "video_file_id_1",
    "video_link_2": "video_file_id_2",
    # لینک‌ها و file_id های مربوط به ویدئوها
}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'سلام! برای دسترسی به ویدئوها، ابتدا باید به کانال ما بپیوندید.')


def check_membership(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_member = context.bot.get_chat_member(
        chat_id=PUBLIC_CHANNEL_USERNAME, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        update.message.reply_text(
            'شما عضو کانال هستید، لطفاً لینک ویدئوی خود را ارسال کنید.')
    else:
        keyboard = [[InlineKeyboardButton(
            "Join Channel", url=f'https://t.me/{PUBLIC_CHANNEL_USERNAME}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'شما عضو کانال نیستید. لطفاً ابتدا به کانال بپیوندید:', reply_markup=reply_markup)


def handle_link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_member = context.bot.get_chat_member(
        chat_id=PUBLIC_CHANNEL_USERNAME, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        video_link = update.message.text
        if video_link in VIDEOS:
            video_file_id = VIDEOS[video_link]
            message = context.bot.send_video(
                chat_id=update.message.chat_id, video=video_file_id)
            time.sleep(20)  # 20 ثانیه صبر می‌کند
            context.bot.delete_message(
                chat_id=update.message.chat_id, message_id=message.message_id)
        else:
            update.message.reply_text('لینک ویدئوی نامعتبر است.')
    else:
        keyboard = [[InlineKeyboardButton(
            "Join Channel", url=f'https://t.me/{PUBLIC_CHANNEL_USERNAME}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'شما عضو کانال نیستید. لطفاً ابتدا به کانال بپیوندید:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, check_membership))
    dispatcher.add_handler(MessageHandler(Filters.entity("url"), handle_link))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
