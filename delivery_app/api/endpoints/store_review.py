from delivery_app.db.schema import StoreReviewSchema
from delivery_app.db.models import StoreReview
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

store_review_router = APIRouter(prefix='/store_review', tags=['Store_reviews'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_review_router.post('/', response_model=StoreReviewSchema)
async def store_review_create(store_review: StoreReviewSchema, db: Session = Depends(get_db)):
    store_review_db = StoreReview(**store_review.dict())
    db.add(store_review_db)
    db.commit()
    db.refresh(store_review_db)
    return store_review_db


@store_review_router.get('/')
async def store_review_list(db: Session = Depends(get_db)):
    return db.query(StoreReview).all()


@store_review_router.get('/{store_review_id}/', response_model=StoreReviewSchema)
async def store_review_detail(store_review_id: int, db: Session = Depends(get_db)):
    store_review_db = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review_db is None:
        raise HTTPException(status_code=404, detail='Store review not found')
    return store_review_db


@store_review_router.put('/{store_review_id}/', response_model=StoreReviewSchema)
async def store_review_update(store_review_id: int, store_review: StoreReviewSchema,
                              db: Session = Depends(get_db)):
    store_review_db = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review_db is None:
        raise HTTPException(status_code=404, detail='Store review not found')

    for store_review_key, store_review_value in store_review.dict().items():
        setattr(store_review_db, store_review_key, store_review_value)

    db.add(store_review_db)
    db.commit()
    db.refresh(store_review_db)
    return store_review_db


@store_review_router.delete('/{store_review_id}/')
async def store_review_delete(store_review_id: int, db: Session = Depends(get_db)):
    store_review_db = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review_db is None:
        raise HTTPException(status_code=404, detail='Store review not found')

    db.delete(store_review_db)
    db.commit()
    return {'message': 'This review is deleted'}
