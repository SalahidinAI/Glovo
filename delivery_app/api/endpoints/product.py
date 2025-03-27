from delivery_app.db.models import Product
from delivery_app.db.schema import ProductSchema
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

product_router = APIRouter(prefix='/product', tags=['Products'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/', response_model=ProductSchema)
async def product_create(product: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/')
async def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}/', response_model=ProductSchema)
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product_db


@product_router.put('/{product_id}/', response_model=ProductSchema)
async def product_update(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.delete('/{product_id}/')
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product_db)
    db.commit()
    return {'message': 'This product is deleted'}
