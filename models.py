from abc import ABC, abstractmethod
from typing import Iterable, Optional, Any, List


class User:
    pk: int


class Sticker:
    pk: str
    uuid: str
    count: int
    tags: List[str]

    def __init__(self, pk, uuid, count, tags):
        self.pk = pk
        self.uuid = uuid
        self.count = count
        self.tags = tags


class GetOrCreateMixin:
    @classmethod
    def get(cls, *args, **kwargs) -> Optional[Any]:
        """ Get the instance (or None) """

    @classmethod
    def create(cls, *args, **kwargs) -> Any:
        """ Create an instance """

    @classmethod
    def get_or_create(cls, *args, **kwargs) -> Any:
        return cls.get(*args, **kwargs) or cls.create(*args, **kwargs)


class BaseUserInterface(GetOrCreateMixin, ABC):

    @staticmethod
    @abstractmethod
    def get_stickers(user) -> Iterable["Sticker"]:
        ...


class BaseStickerInterface(GetOrCreateMixin, ABC):

    @staticmethod
    @abstractmethod
    def increment_count(sticker_id, user_id, by=1):
        ...

    @staticmethod
    @abstractmethod
    def add_tags(sticker_id, user_id, tags: Iterable[str]):
        ...
