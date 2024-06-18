from app.database import crud, schemas, tables


def get_devices(db, brand_id: int):
    conditions = [
        schemas.QueryForm(key="brand_id", operator="==", value=brand_id),
    ]
    return crud.selects(db, tables.Device, conditions)
