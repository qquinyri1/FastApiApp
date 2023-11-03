from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.schemas import ContactModel, ContactResponse, UpdateContactDate
from src.database.models import User
from src.repository import contacts as repository_contacts

from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit,current_user, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    name: str = None,
    current_user: User = Depends(auth_service.get_current_user),
    surname: str = None,
    email: str = None,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(current_user,name, surname, email,db)
    if contacts == []:
        raise HTTPException(status_code=400, detail="No contacts found :(")
    elif isinstance(contacts, str):
        raise HTTPException(status_code=400, detail=contacts)
    return contacts


@router.get("/upcoming", response_model=List[ContactResponse])
async def get_upcoming_contacts(days: int = 7, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.get_contacts_within_next_week(days, current_user,db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user,db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    result = await repository_contacts.create_contact(body, current_user,db)

    if result is None:
        raise HTTPException(
            status_code=400, detail=f"Contact already exists."
        )

    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)

    return result


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.update_general_contact(contact_id, body,current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}/date", response_model=ContactResponse)
async def update_contact_date(
    date_body: UpdateContactDate, contact_id: int, db: Session = Depends(get_db), 
    current_user: User = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.update_contact_birthday(
        contact_id, date_body,current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found or doesn't have a 'birthday' value.",
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user,db)
    if contact is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact