from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.ticket import get_comments, get_minutes, check_work, start_work, end_work

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for Ticket.


# Get all tickets.
@router.get("/", response_model=list[schemas.Ticket])
async def select_tickets(
        db: databaseSession,
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:list"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    tickets = db.scalars(stmt).all()
    return tickets


# Get ticket by id.
@router.get("/{ticket_id}", response_model=schemas.Ticket)
async def select_ticket(
        db: databaseSession,
        ticket_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:info"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )
    ticket.comments = get_comments(db, ticket)
    ticket.work_times = get_minutes(db, ticket)
    ticket.creator = common.get_creator(db, ticket.creator_id)
    return ticket


# Create ticket.
@router.post("/", response_model=schemas.Ticket)
async def create_ticket(
        db: databaseSession,
        form_data: schemas.TicketCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:create"]),
):
    form_data.creator_id = current_user.id
    ticket = tables.Ticket(**form_data.model_dump())
    db.add(ticket)
    db.commit()
    return ticket


# Update ticket.
@router.put("/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(
        db: databaseSession,
        ticket_id: int,
        form_data: list[schemas.UpdateForm],
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:update"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )
    for form in form_data:
        setattr(ticket, form.key, form.value)
    db.commit()
    return ticket


# Delete ticket.
@router.delete("/{ticket_id}", response_model=schemas.Ticket)
async def delete_ticket(
        db: databaseSession,
        ticket_id: int,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:delete"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )

    setattr(ticket, "deleter_id", current_user.id)
    setattr(ticket, "deleted_at", common.now())
    db.commit()
    return ticket


# Create ticket comment.
@router.post("/{ticket_id}/comments", response_model=schemas.TicketComment)
async def create_ticket_has_comments(
        db: databaseSession,
        ticket_id: int,
        form_data: schemas.TicketCommentCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:comment"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )

    form_data.ticket_id = ticket.id
    form_data.creator_id = current_user.id
    comment = tables.TicketComment(**form_data.model_dump())
    db.add(comment)
    db.commit()
    return comment


# Start work on ticket.
@router.post("/{ticket_id}/start_work", response_model=schemas.TicketMinute)
async def start_work_on_ticket(
        db: databaseSession,
        ticket_id: int,
        form_data: schemas.TicketMinuteCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:work"]),
):
    if ticket_id != form_data.ticket_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Ticket id not match.",
        )
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )

    minute = check_work(db, ticket, current_user)
    if minute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Work on ticket already exists.",
        )

    minute = start_work(db, ticket, current_user, form_data.message or None)
    return minute


# End work on ticket.
@router.post("/{ticket_id}/end_work", response_model=schemas.TicketMinute)
async def end_work_on_ticket(
        db: databaseSession,
        ticket_id: int,
        form_data: schemas.TicketMinuteCreateForm,
        current_user: schemas.User = Security(get_current_user, scopes=["ticket:work"]),
):
    if ticket_id != form_data.ticket_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Ticket id not match.",
        )
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.id.__eq__(ticket_id))
    )
    ticket = db.scalars(stmt).one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not exists.",
        )

    minute = check_work(db, ticket, current_user)
    if not minute:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Work on ticket not exists.",
        )

    minute = end_work(db, ticket, current_user, form_data.message)
    return minute
