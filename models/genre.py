'''define Genre model'''
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.basemodel import Basemodel, Base
from models.book import Book

class Genre(Basemodel, Base):
    '''Genre model'''
    __tablename__ = 'genres'
    name = Column(String(250), nullable=False, unique=True)
    books = relationship("Book", backref="genre")
    
    def __init__(self, *args, **kwargs):
        '''constructor'''
        super().__init__(*args, **kwargs)

    def get_books(self):
        '''get books of the genre'''
        from models import storage
        return storage.session.query(Book).filter(self.id == Book.genre_id).all()
