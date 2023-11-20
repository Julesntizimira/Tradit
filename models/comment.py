#!/usr/bin/python3

from models.basemodel import Basemodel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


class Comment(Basemodel, Base):
    __tablename__ = 'comments'
    text = Column(String(500), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(60), ForeignKey("books.id"), nullable=False)

    number = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = Comment.number + 1
