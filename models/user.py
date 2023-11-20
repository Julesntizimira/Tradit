#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship
from models.basemodel import Basemodel, Base
from models.comment import Comment


class User(Basemodel, Base):
    __tablename__ = 'users'
    name = Column(String(250), nullable=False)
    address = Column(String(60), nullable=False)
    comments = relationship("Comment", backref="user", cascade="all, delete-orphan")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_comments(self):
        from models import storage
        return storage.session.query(Comment).filter(Comment.id == self.id).all()
