from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship
from models.basemodel import Basemodel, Base
from models.book import Book

class Genre(Basemodel, Base):
    __tablename__ = 'genres'
    name = Column(String(250), nullable=False)
    books = relationship("Book", backref="genre")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_books(self):
        from models import storage
        return storage.session.query(Book).filter(self.id == Book.genre_id).all()
