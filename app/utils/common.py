from datetime import datetime

from sqlalchemy import select

from app.database import tables, schemas


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


def check_asset_number(db, asset_number):
    stmt = (
        select(tables.AssetNumber)
        .where(tables.AssetNumber.deleted_at.is_(None))
        .where(tables.AssetNumber.number.__eq__(asset_number))
    )
    asset_number = db.scalars(stmt).one_or_none()
    if asset_number:
        return True
    return False
