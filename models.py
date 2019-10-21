from pony.orm import Database, Required, Optional, Set, StrArray

db = Database(provider='sqlite', filename='database.sqlite', create_db=True)


class User(db.Entity):
    pk = Required(int)
    stickers = Set("Sticker")


class Sticker(db.Entity):
    pk = Required(str)
    uuid = Required(str)
    count = Optional(int)
    tags = Optional(StrArray)

    user = Required(User)


db.generate_mapping(create_tables=True)

