from delivery_app.db.models import Combo
from delivery_app.db.schema import ComboSchema
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

combo_router = APIRouter(prefix='/combo', tags=['Combos'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@combo_router.post('/', response_model=ComboSchema)
async def combo_create(combo: ComboSchema, db: Session = Depends(get_db)):
    combo_db = Combo(**combo.dict())
    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return combo_db


@combo_router.get('/')
async def combo_list(db: Session = Depends(get_db)):
    return db.query(Combo).all()


@combo_router.get('/{combo_id}/', response_model=ComboSchema)
async def combo_detail(combo_id: int, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Combo not found')
    return combo_db


@combo_router.put('/{combo_id}/', response_model=ComboSchema)
async def combo_update(combo_id: int, combo: ComboSchema, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Combo not found')

    for combo_key, combo_value in combo.dict().items():
        setattr(combo_db, combo_key, combo_value)

    db.add(combo_db)
    db.commit()
    db.refresh(combo_db)
    return combo_db


@combo_router.delete('/{combo_id}/')
async def combo_delete(combo_id: int, db: Session = Depends(get_db)):
    combo_db = db.query(Combo).filter(Combo.id == combo_id).first()
    if combo_db is None:
        raise HTTPException(status_code=404, detail='Combo not found')

    db.delete(combo_db)
    db.commit()
    return {'message': 'This Combo is deleted'}
