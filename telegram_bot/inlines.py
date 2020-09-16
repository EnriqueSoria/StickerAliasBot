from telegram import InlineQueryResultCachedSticker

from database.pony.interface import UserInterface, StickerInterface


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query.lower().strip()

    user_pk = update.inline_query.from_user.id
    results = []

    context.user_data['stickers'] = {}
    for sticker in UserInterface.get_stickers(user_pk):
        if len(query) < 2 or query in sticker.tags:
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

    sticker = StickerInterface.get(
        sticker_id=sticker_uuid,
        user_id=user_pk
    )
    StickerInterface.increment_count(sticker)
