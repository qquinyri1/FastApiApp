from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.schemas import Contactt, ContactResponse, Update

from src.repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    name: str = None,
    surname: str = None,
    email: str = None,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(name, surname, email, db)
    if contacts == []:
        raise HTTPException(status_code=400, detail="No contacts found :(")
    elif isinstance(contacts, str):
        raise HTTPException(status_code=400, detail=contacts)
    return contacts


@router.get("/upcoming", response_model=List[ContactResponse])
async def get_upcoming_contacts(days: int = 7, db: Session = Depends(get_db)):
    return await repository_contacts.get_contacts_within_next_week(days, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: Contactt, db: Session = Depends(get_db)):
    result = await repository_contacts.create_contact(body, db)

    if result is None:
        raise HTTPException(
            status_code=400, detail=f"Contact with name '{body.name}' already exists."
        )

    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)

    return result


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: Contactt, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_general_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}/date", response_model=ContactResponse)
async def update_contact_date(
    date_body: Update, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact_birthday(
        contact_id, date_body, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found or doesn't have a 'birthday' value.",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact