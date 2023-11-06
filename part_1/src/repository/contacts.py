from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param skip: int: Skip a number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.
        Args:
            contact_id (int): The id of the contact to retrieve.
            user (User): The user who owns the requested Contact.
            db (Session): A database session object for querying and updating data in our database.
    
    :param contact_id: int: Specify the id of the contact we want to get
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactBase: Pass the data from the request body to the function
    :param user: User: Get the user_id from the user object and  representing the owner of the contact
    :param db: Session: Access the database
    :return: A newly created contact object
    """
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
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactBase): The updated information for the specified user's contact.
            user (User): The current logged-in user, used to verify that they are updating their own data and not someone else's data.
            db (Session): A connection to our database, used for querying and committing changes.
    
    :param contact_id: int: Specify which contact to update
    :param body: ContactBase: Get the data from the request body
    :param user: User: Ensure that the user is only able to update contacts that they have created
    :param db: Session: Access the database
    :return: A contact object if the contact is updated, else None;
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name=body.first_name, 
        contact.last_name=body.last_name, 
        contact.email=body.email, 
        contact.phone_number=body.phone_number, 
        contact.birthday=body.birthday, 
        contact.additional_data=body.additional_data
        contact.user_id=user.id
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session)  -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts being removed.
            db (Session): A connection to our database, used for querying and deleting data.
    
    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A contact object, so the return type should be contact
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, user: User, db: Session) -> List[Contact]:
    """
    The search_contacts function searches for contacts by first name, last name, and email.
        It returns a list of all the contacts that match the query.
    
    :param query: str: Search the database for a contact
    :param user: User: Get the user id to filter out contacts that don't belong to the current user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
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
    """
    The get_birthday_per_week function returns a list of contacts whose birthday is within the next 7 days.
        Args:
            days (int): The number of days to look ahead for birthdays. Default is 7.
            user (User): The User object that owns the contact list being queried.
            db (Session): A database session object used to query the database for contacts belonging to a specific user.
    
    :param days: int: Specify the number of days in which we want to get all contacts with birthdays
    :param user: User: The User object that owns the contacts
    :param db: Session: Access the database
    :return: A list of contacts, but the return type is contact
    """
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in all_contacts:
        if timedelta(0) <= ((contact.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(contact)

    return response