from delivery_app.db.schema import CourierReviewSchema
from delivery_app.db.models import CourierReview
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

courier_review_router = APIRouter(prefix='/courier_review', tags=['Courier_reviews'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@courier_review_router.post('/', response_model=CourierReviewSchema)
async def courier_review_create(courier_review: CourierReviewSchema, db: Session = Depends(get_db)):
    courier_review_db = CourierReview(**courier_review.dict())
    db.add(courier_review_db)
    db.commit()
    db.refresh(courier_review_db)
    return courier_review_db


@courier_review_router.get('/')
async def courier_review_list(db: Session = Depends(get_db)):
    return db.query(CourierReview).all()


@courier_review_router.get('/{courier_review_id}/')
async def courier_review_detail(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review_db = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review_db is None:
        raise HTTPException(status_code=404, detail='Courier review not found')
    return courier_review_db


@courier_review_router.put('/{courier_review_id}/', response_model=CourierReviewSchema)
async def courier_review_update(courier_review_id: int, courier_review: CourierReviewSchema,
                                db: Session = Depends(get_db)):
    courier_review_db = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review_db is None:
        raise HTTPException(status_code=404, detail='Courier review not found')

    for courier_review_key, courier_review_value in courier_review.dict().items():
        setattr(courier_review_db, courier_review_key, courier_review_value)

    db.add(courier_review_db)
    db.commit()
    db.refresh(courier_review_db)
    return courier_review_db


@courier_review_router.delete('/{courier_review_id}/')
async def courier_review_delete(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review_db = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review_db is None:
        raise HTTPException(status_code=404, detail='Courier review not found')

    db.delete(courier_review_db)
    db.commit()
    return {'message': 'This review is deleted'}
