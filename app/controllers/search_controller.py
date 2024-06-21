from typing import Union

from fastapi import APIRouter, HTTPException, status, Security
from sqlalchemy import select

from ..dependencies import get_oauth_scheme, get_current_user, databaseSession
from ..database import schemas, tables
from ..utils import common
from ..services.role import get_users, get_historical_users

oauth2_scheme = get_oauth_scheme()

router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# APIs for search.


# Search by asset number.
@router.get("/assets/asset_number/{asset_number}", response_model=Union[schemas.Device])
async def select_asset_number(
        db: databaseSession,
        asset_number: str,
        current_user: schemas.User = Security(get_current_user, scopes=["search:asset_number"]),
):
    stmt = (
        select(tables.AssetNumber)
        .where(tables.AssetNumber.deleted_at.is_(None))
        .where(tables.AssetNumber.number.__eq__(asset_number))
    )
    asset_number = db.scalars(stmt).one_or_none()
    if not asset_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset number not exists.",
        )

    table = getattr(tables, asset_number.table_name)

    stmt = (
        select(table)
        .where(table.deleted_at.is_(None))
        .where(table.id.__eq__(asset_number.table_id))
    )
    asset = db.scalars(stmt).one_or_none()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not exists.",
        )
    asset.creator = common.get_creator(db, asset.creator_id)
    return asset


@router.get("/tickets/title/{keyword}", response_model=list[schemas.Ticket])
async def select_tickets(
        db: databaseSession,
        keyword: str,
        current_user: schemas.User = Security(get_current_user, scopes=["search:ticket"]),
):
    stmt = (
        select(tables.Ticket)
        .where(tables.Ticket.deleted_at.is_(None))
        .where(tables.Ticket.title.ilike(f"%{keyword}%"))
    )
    tickets = db.scalars(stmt).all()
    return tickets
