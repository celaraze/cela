from datetime import datetime

from sqlalchemy import select

from app.database import tables


def now():
    now_string = datetime.now()
    return now_string.strftime("%Y-%m-%d %H:%M:%S")


def get_creator(db, creator_id):
    stmt = (
        select(tables.User)
        .where(tables.User.id.__eq__(creator_id))
    )
    user = db.scalars(stmt).one_or_none()
    return user
