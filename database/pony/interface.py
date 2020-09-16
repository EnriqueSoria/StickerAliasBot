from typing import Iterable
from uuid import uuid4

from pony.orm import select, db_session

import models
from database.pony.models import PonySticker, PonyUser


class UserInterface(models.BaseUserInterface):
    @classmethod
    def get(cls, user_id) -> "User":
        with db_session:
            return PonyUser.get(pk=user_id)

    @classmethod
    def create(cls, user_id) -> "User":
        with db_session:
            return PonyUser(pk=user_id)

    @staticmethod
    def get_stickers(user_id) -> Iterable[models.Sticker]:
        with db_session:
            sticker_list = select(s for s in PonySticker if s.user.pk == user_id).order_by(lambda s: -s.count)
            return [
                models.Sticker(
                    pk=sticker.pk,
                    uuid=sticker.uuid,
                    count=sticker.count,
                    tags=sticker.tags
                ) for sticker in sticker_list
            ]


class StickerInterface(models.BaseStickerInterface):

    @classmethod
    def get(cls, sticker_id, user_id):
        with db_session:
            user = UserInterface.get(user_id)
            return PonySticker.get(pk=sticker_id, user=user)

    @classmethod
    def create(cls, sticker_id, user_id):
        with db_session:
            user = UserInterface.get(user_id)
            return PonySticker(
                pk=sticker_id,
                user=user,
                count=0,
                uuid=str(uuid4().int),
            )

    @staticmethod
    def increment_count(sticker_id, user_id, by=1):
        with db_session:
            sticker = StickerInterface.get(sticker_id, user_id)
            sticker.count += 1

    @staticmethod
    def add_tags(sticker_id, user_id, tags: Iterable[str]):
        with db_session:
            sticker = StickerInterface.get(sticker_id, user_id)
            sticker.tags = tags
