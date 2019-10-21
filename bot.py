#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from uuid import uuid4

from pony.orm import db_session, select, commit
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent,
                      ParseMode, InlineQueryResultCachedSticker)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, InlineQueryHandler, ChosenInlineResultHandler)
from telegram.utils.helpers import escape_markdown

import models

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

STICKER, TAGS, *_ = range(10)


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query.lower().strip()

    user_pk = update.inline_query.from_user.id
    results = []

    context.user_data['stickers'] = {}
    with db_session:
        for sticker in select(s for s in models.Sticker if s.user.pk == user_pk).order_by(lambda s: -s.count):
            if len(query) < 2:
                results.append(
                    InlineQueryResultCachedSticker(
                        id=sticker.uuid,
                        sticker_file_id=sticker.pk,
                    )
                )
            elif query in sticker.tags:
                results.append(
                    InlineQueryResultCachedSticker(
                        id=sticker.uuid,
                        sticker_file_id=sticker.pk,
                    )
                )

    update.inline_query.answer(results[:10])


def inlinefeedback(update, context):
    user_pk = update.chosen_inline_result.from_user.id
    sticker_uuid = update.chosen_inline_result.result_id

    with db_session:
        user = models.User.get(pk=user_pk)
        sticker = models.Sticker.get(uuid=sticker_uuid, user=user)
        sticker.count += 1


def start(update, context):
    update.message.reply_text(
        """Hola, enviam un sticker.""",
    )

    # register user
    with db_session:
        pk = update.message.from_user.id
        user = models.User.get(pk=pk)
        if user is None:
            user = models.User(pk=pk)

    return STICKER


def rcv_sticker(update, context):
    pk = update.message.from_user.id
    sticker_id = update.message.sticker.file_id

    with db_session:
        user = models.User.get(pk=pk)
        sticker = models.Sticker.get(user=user, pk=sticker_id)
        context.user_data['sticker'] = sticker_id
        if sticker is None:
            sticker = models.Sticker(
                pk=sticker_id,
                count=0,
                uuid=str(uuid4().int),
                user=user
            )

    update.message.reply_text(
        """Vale, ara enviam una serie de paraules que el definixquen (separades per espais)"""
    )

    return TAGS


def rcv_tags(update, context):
    tags = update.message.text.lower().split(' ')
    pk = update.message.from_user.id

    with db_session:
        user = models.User.get(pk=pk)
        sticker = models.Sticker.get(user=user, pk=context.user_data['sticker'])
        sticker.tags = tags
        del context.user_data['sticker']

    update.message.reply_text('Vale, ja està!')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    secret = ''
    with open('.secret', 'r') as dotsecret:
        secret = dotsecret.read().strip()
    updater = Updater(secret, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            STICKER: [MessageHandler(Filters.sticker, rcv_sticker)],

            TAGS: [MessageHandler(Filters.text, rcv_tags)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(inlinefeedback))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
