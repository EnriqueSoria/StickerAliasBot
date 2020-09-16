from pony.orm import db_session
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from database.pony.interface import UserInterface, StickerInterface
from settings import logger
from telegram_bot.enumerations import STICKER, TAGS


def start(update, context):
    update.message.reply_text(
        """Hola, enviam un sticker.""",
    )

    pk = update.message.from_user.id
    UserInterface.get_or_create(user_id=pk)

    return STICKER


@db_session
def rcv_sticker(update, context):
    user_pk = update.message.from_user.id
    sticker_id = update.message.sticker.file_id

    StickerInterface.get_or_create(
        sticker_id=sticker_id,
        user_id=user_pk
    )
    context.user_data['sticker'] = sticker_id

    update.message.reply_text(
        """Vale, ara enviam una serie de paraules que el definixquen (separades per espais)"""
    )

    return TAGS


def rcv_tags(update, context):
    tags = update.message.text.lower().split(' ')
    user_pk = update.message.from_user.id
    sticker_pk = context.user_data['sticker']

    StickerInterface.add_tags(sticker_id=sticker_pk, user_id=user_pk, tags=tags)
    del context.user_data['sticker']

    update.message.reply_text('Vale, ja està!')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Operació cancel·lada',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
