#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship
from models.basemodel import Basemodel, Base
from models.book import Book


class Author(Basemodel, Base):
    __tablename__ = 'authors'
    name = Column(String(250), nullable=False)
    biography = Column(String(250))
    books = relationship("Book", backref="author", cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    def get_books(self):
        from models import storage
        return storage.session.query(Book).filter(self.id == Book.author_id).all()
