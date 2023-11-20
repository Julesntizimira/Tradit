from models.basemodel import Basemodel, Base
from models.comment import Comment
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Book(Basemodel, Base):
    __tablename__ = 'books'
    title = Column(String(250), nullable=False)
    release_date = Column(Integer, nullable=False) 
    author_id = Column(String(60), ForeignKey("authors.id"), nullable=False) 
    genre_id = Column(String(60), ForeignKey("genres.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    description = Column(String(500), nullable=False)
    comments = relationship("Comment", backref="book", cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_comments(self):
        from models import storage
        return storage.session.query(Comment).filter(Comment.id == self.id).all()
