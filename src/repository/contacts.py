from typing import List, Optional, Union
from datetime import date, timedelta
from sqlalchemy import and_
from sqlalchemy.sql.expression import extract
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from src.database.models import Contact, User
from src.schemas.schemas import ContactModel, UpdateContactDate
from src.database.db import get_db
from sqlalchemy.orm import Session


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter_by(user_id=user.id).offset(skip).limit(limit).all()


async def search_contacts(
    user: User,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Union[List[Contact], str]:
    query = db.query(Contact).filter_by(user_id=user.id)

    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Contact.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    results = query.all()
    if not results:
        return "No contacts found "
    return results


async def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Union[Contact, None, str]:
    existing_contact = db.query(Contact).filter_by(user_id=user.id, email=body.email).first()
    if existing_contact:
        return None
    
    new_contact = Contact(**body.dict(), user_id=user.id)
    db.add(new_contact)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        return str(e)
    
    db.refresh(new_contact)
    return new_contact


async def update_general_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Optional[Contact]:
    contact = await get_contact(contact_id, user, db)
    if not contact:
        return None
    
    for field, value in body.dict().items():
        if value is not None:
            setattr(contact, field, value)
    
    db.commit()
    return contact


async def update_contact_birthday(contact_id: int, date_body: UpdateContactDate, user: User, db: Session) -> Optional[Contact]:
    contact = await get_contact(contact_id, user, db)
    if not contact or not contact.birthday:
        return None
    
    try:
        new_date = contact.birthday.replace(year=date_body.year, month=date_body.month, day=date_body.day)
    except ValueError:
        if date_body.month == 2 and date_body.day == 29:
            new_date = contact.birthday.replace(year=date_body.year, month=2, day=28)
        else:
            return None  
    
    contact.birthday = new_date
    db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    contact = await get_contact(contact_id, user, db)
    if not contact:
        return None
    
    db.delete(contact)
    db.commit()
    return contact


async def get_contacts_within_next_week(days: int, user: User, db: Session) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=days)

    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            extract("year", Contact.birthday) == today.year,
            Contact.birthday.between(today, end_date)
        )
    ).all()