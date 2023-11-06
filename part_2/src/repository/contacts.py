from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    contact = Contact(
    first_name=body.first_name, 
    last_name=body.last_name, 
    email=body.email, 
    phone_number=body.phone_number, 
    birthday=body.birthday, 
    additional_data=body.additional_data,
    user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, user: User, db: Session) -> Contact| None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name=body.first_name, 
        contact.last_name=body.last_name, 
        contact.email=body.email, 
        contact.phone_number=body.phone_number, 
        contact.birthday=body.birthday, 
        contact.additional_data=body.additional_data
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, user: User, db: Session) -> List[Contact]:
    response = []
    search_by_first_name = db.query(Contact).filter(and_(Contact.first_name.like(f'%{query}%'), Contact.user_id == user.id)).all()
    if search_by_first_name:
        for i in search_by_first_name:
            response.append(i)
    search_by_last_name = db.query(Contact).filter(and_(Contact.last_name.like(f'%{query}%'), Contact.user_id == user.id)).all()
    if search_by_last_name:
        for i in search_by_last_name:
            response.append(i)
    search_by_email = db.query(Contact).filter(and_(Contact.email.like(f'%{query}%'), Contact.user_id == user.id)).all()
    if search_by_email:
        for i in search_by_email:
            response.append(i)
            
    return response


async def get_birthday_per_week(days: int, user: User, db: Session) -> Contact:
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in all_contacts:
        if timedelta(0) <= ((contact.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(contact)
    return response