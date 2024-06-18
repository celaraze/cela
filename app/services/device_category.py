from app.database import crud, schemas, tables


def get_devices(db, category_id: int):
    conditions = [
        schemas.QueryForm(key="category_id", operator="==", value=category_id),
    ]
    return crud.selects(db, tables.Device, conditions)
