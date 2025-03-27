from delivery_app.db.schema import OrderSchema
from delivery_app.db.models import Order
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

order_router = APIRouter(prefix='/order', tags=['Orders'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_router.post('/', response_model=OrderSchema)
async def order_create(order: OrderSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get('/')
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}/', response_model=OrderSchema)
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')
    return order_db


@order_router.put('/{order_id}/', response_model=OrderSchema)
async def order_update(order_id: int, order: OrderSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')

    for order_key, order_value in order.dict().items():
        setattr(order_db, order_key, order_value)

    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.delete('/{order_id}/')
async def order_delete(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if order_db is None:
        raise HTTPException(status_code=404, detail='Order not found')

    db.delete(order_db)
    db.commit()
    return {'message': 'This order is deleted'}
