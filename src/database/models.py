from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    birthday = Column(Date, default=datetime.utcnow)
    extra_info = Column(String, nullable=True)


