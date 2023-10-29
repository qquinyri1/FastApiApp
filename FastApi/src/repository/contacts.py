from typing import List, Optional, Union

from src.database.models import Contact
from src.schemas.schemas import Contactt, Update

from fastapi import Depends

from src.database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def search_contacts(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[Contact]:
    if name is not None:
        return db.query(Contact).filter(Contact.name == name).all()
    elif surname is not None:
        return db.query(Contact).filter(Contact.surname.ilike(f"%{surname}%")).all()
    elif email is not None:
        return db.query(Contact).filter(Contact.email.ilike(f"%{email}%")).all()
    else:
        return "Either 'name' or 'contact_id' must be provided."


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: Contactt, db: Session) -> Union[Contact, None, str]:
    existing_contact = db.query(Contact).filter(Contact.email == body.email).first()
    if existing_contact:
        return None

    contact = Contact(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        extra_info=body.extra_info,
    )
    db.add(contact)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        return str(e)
    db.refresh(contact)
    return contact


async def update_general_contact(
    contact_id: int, body: Contactt, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        if body.name:
            contact.name = body.name
        if body.surname:
            contact.surname = body.surname
        if body.email:
            contact.email = body.email
        if body.phone_number:
            contact.phone_number = body.phone_number
        if body.birthday:
            contact.birthday = body.birthday
        if body.extra_info:
            contact.extra_info = body.extra_info

        db.commit() 

        return contact

    return None


async def update_contact_birthday(
    contact_id: int, date_body: Update, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact or not contact.birthday:
        return None

    try:
        new_date = contact.birthday.replace(
            year=date_body.year, month=date_body.month, day=date_body.day
        )
    except ValueError:

        if (
            date_body.month == 2
            and date_body.day == 29
            and not date(date_body.year, 2, 29).strftime("%Y-%m-%d")
        ):
            new_date = contact.birthday.replace(year=date_body.year, month=2, day=28)
        else:
            raise

    contact.birthday = new_date
    db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


from datetime import date, timedelta
from sqlalchemy.sql.expression import extract


async def get_contacts_within_next_week(days: int, db: Session) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=days)

    return (
        db.query(Contact)
        .filter(
            extract("year", Contact.birthday) == today.year,
            Contact.birthday >= today,
            Contact.birthday < end_date,
        )
        .all()
    )