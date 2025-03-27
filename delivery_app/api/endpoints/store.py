from delivery_app.db.models import Store
from delivery_app.db.schema import StoreSchema
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

store_router = APIRouter(prefix='/store', tags=['Stores'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_router.post('/', response_model=StoreSchema)
async def store_create(store: StoreSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.get('/')
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()


@store_router.get('/{store_id}/', response_model=StoreSchema)
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Store not found')
    return store_db


@store_router.put('/{store_id}/', response_model=StoreSchema)
async def store_update(store_id: int, store: StoreSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Store not found')

    for store_key, store_value in store.dict().items():
        setattr(store_db, store_key, store_value)

    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@store_router.delete('/{store_id}/')
async def store_delete(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail='Store not found')
    db.delete(store_db)
    db.commit()
    return {'message': 'This store is deleted'}
