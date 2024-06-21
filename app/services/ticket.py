from app.utils import common
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


def get_work_times(db, ticket):
    stmt = (
        select(tables.TicketWorkTime)
        .where(tables.TicketWorkTime.deleted_at.is_(None))
        .where(tables.TicketWorkTime.ticket_id.__eq__(ticket.id))
    )
    work_times = db.scalars(stmt).all()
    return work_times


def check_work(db, ticket, user):
    stmt = (
        select(tables.TicketWorkTime)
        .where(tables.TicketWorkTime.deleted_at.is_(None))
        .where(tables.TicketWorkTime.ticket_id.__eq__(ticket.id))
        .where(tables.TicketWorkTime.creator_id.__eq__(user.id))
        .where(tables.TicketWorkTime.flag.__eq__(0))
    )
    work_time = db.scalars(stmt).one_or_none()
    return work_time


def start_work(db, ticket, user, message=None):
    form_data = schemas.TicketWorkTimeCreateForm(
        ticket_id=ticket.id,
        flag=0,
        message=message,
        creator_id=user.id,
    )
    work_time = tables.TicketWorkTime(**form_data.model_dump())
    db.add(work_time)
    db.commit()
    return work_time


def end_work(db, ticket, user, message=None):
    form_data = schemas.TicketWorkTimeCreateForm(
        ticket_id=ticket.id,
        flag=1,
        message=message,
        creator_id=user.id,
    )
    work_time = tables.TicketWorkTime(**form_data.model_dump())
    db.add(work_time)
    db.commit()
    return work_time
