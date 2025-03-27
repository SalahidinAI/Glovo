from delivery_app.db.models import Contact
from delivery_app.db.schema import ContactSchema
from delivery_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

contact_router = APIRouter(prefix='/contact', tags=['Contacts'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contact_router.post('/', response_model=ContactSchema)
async def contact_create(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = Contact(**contact.dict())
    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@contact_router.get('/')
async def contact_list(db: Session = Depends(get_db)):
    return db.query(Contact).all()


@contact_router.get('/{contact_id}/', response_model=ContactSchema)
async def contact_detail(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')
    return contact_db


@contact_router.put('/{contact_id}/', response_model=ContactSchema)
async def contact_update(contact_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')

    for contact_key, contact_value in contact.dict().items():
        setattr(contact_db, contact_key, contact_value)

    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db


@contact_router.delete('/{contact_id}/')
async def contact_delete(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact_db is None:
        raise HTTPException(status_code=404, detail='Contact not found')

    db.delete(contact_db)
    db.commit()
    return {'message': 'This contact is deleted'}
