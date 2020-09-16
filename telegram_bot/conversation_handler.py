from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from telegram_bot.commands import rcv_tags, cancel, start, rcv_sticker
from telegram_bot.enumerations import STICKER, TAGS

sticker_alias_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        STICKER: [MessageHandler(Filters.sticker, rcv_sticker)],
        TAGS: [MessageHandler(Filters.text, rcv_tags)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
