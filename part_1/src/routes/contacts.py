from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_new_contact(body: ContactBase, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_new_contact function creates a new contact in the database.
        The function takes a ContactBase object as input, which is then used to create the new contact.
        The current_user variable is used to determine who created this contact.
    
    :param body: ContactBase: Get the data from the request body
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user who is making the request
    :return: A contactbase object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/all", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_all_contacts function returns a list of contacts.
        The function takes in an optional skip and limit parameter to paginate the results.
        
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact_by_id(contact_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact_by_id function returns a contact by its id.
        If the user is not logged in, an HTTP 401 Unauthorized error is returned.
        If the user does not have access to this contact, an HTTP 403 Forbidden error is returned.
        If no such contact exists with that id, an HTTP 404 Not Found error is returned.
    
    :param contact_id: int: Specify the contact id to be retrieved from the database
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object, which is a pydantic model
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactBase object containing the new values for the contact.
            - contact_id: An integer representing the id of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a database, defaults to None if not provided. 
                If no session is provided, one will be created using get_db().
    
    :param body: ContactBase: Pass the data that will be used to update the contact
    :param contact_id: int: Identify the contact
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user information
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_user(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_user function removes a user from the database.
        Args:
            contact_id (int): The id of the user to be removed.
            db (Session, optional): A database session object for interacting with the database. Defaults to Depends(get_db).
            current_user (User, optional): The currently logged in user object. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Specify the contact id of the user we want to remove
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/find/{query}", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def find_contacts(query: str, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The find_contacts function searches for contacts in the database.
        The function takes a query string and returns a list of contacts that match the query.
        If no contact is found, an HTTP 404 error is returned.
    
    :param query: str: Search for contacts that match the query string
    :param db: Session: Get the database connection
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def contacts_birthday(days: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The contacts_birthday function returns a list of contacts that have birthdays within the next 7 days.
        The function takes in an integer value for the number of days to search for and returns a list of contacts
        with birthdays within that range.
    
    :param days: int: Specify the number of days to look for contacts with birthdays
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user who is logged in
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday_per_week(days, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts