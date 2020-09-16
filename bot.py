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

from telegram.ext import (Updater, InlineQueryHandler, ChosenInlineResultHandler)

# Enable logging
import settings
from telegram_bot.conversation_handler import sticker_alias_handler
from telegram_bot.inlines import inlinequery, inlinefeedback


def error(update, context):
    """Log Errors caused by Updates."""
    settings.logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(sticker_alias_handler)
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(inlinefeedback))
    dp.add_error_handler(error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
