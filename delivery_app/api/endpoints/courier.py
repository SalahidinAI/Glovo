from delivery_app.db.schema import CourierSchema
from delivery_app.db.models import Courier
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

courier_router = APIRouter(prefix='/courier', tags=['Couriers'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@courier_router.post('/', response_model=CourierSchema)
async def courier_create(courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/')
async def courier_list(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}/', response_model=CourierSchema)
async def courier_detail(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')
    return courier_db


@courier_router.put('/{courier_id}/', response_model=CourierSchema)
async def courier_update(courier_id: int, courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')

    for courier_key, courier_value in courier.dict().items():
        setattr(courier_db, courier_key, courier_value)

    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.delete('/{courier_id}/')
async def courier_delete(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier_db is None:
        raise HTTPException(status_code=404, detail='Courier not found')

    db.delete(courier_db)
    db.commit()
    return {'message': 'This courier is deleted'}
