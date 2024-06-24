from sqlalchemy import select

from app.database import tables, schemas


def get_comments(db, ticket):
    stmt = (
        select(tables.TicketComment)
        .where(tables.TicketComment.deleted_at.is_(None))
        .where(tables.TicketComment.ticket_id.__eq__(ticket.id))
    )
    comments = db.scalars(stmt).all()
    return comments


def get_minutes(db, ticket):
    stmt = (
        select(tables.TicketMinute)
        .where(tables.TicketMinute.deleted_at.is_(None))
        .where(tables.TicketMinute.ticket_id.__eq__(ticket.id))
    )
    minutes = db.scalars(stmt).all()
    return minutes


def check_work(db, ticket, user):
    stmt = (
        select(tables.TicketMinute)
        .where(tables.TicketMinute.deleted_at.is_(None))
        .where(tables.TicketMinute.ticket_id.__eq__(ticket.id))
        .where(tables.TicketMinute.creator_id.__eq__(user.id))
        .where(tables.TicketMinute.flag.__eq__(0))
    )
    minute = db.scalars(stmt).one_or_none()
    return minute


def start_work(db, ticket, user, message):
    form_data = schemas.TicketMinuteCreateForm(
        ticket_id=ticket.id,
        flag=0,
        message=message,
        creator_id=user.id,
    )
    minute = tables.TicketMinute(**form_data.model_dump())
    db.add(minute)
    db.commit()
    return minute


def end_work(db, ticket, user, message):
    form_data = schemas.TicketMinuteCreateForm(
        ticket_id=ticket.id,
        flag=1,
        message=message,
        creator_id=user.id,
    )
    minute = tables.TicketMinute(**form_data.model_dump())
    db.add(minute)
    db.commit()
    return minute
