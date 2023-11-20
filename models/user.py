from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.basemodel import Basemodel, Base
from models.comment import Comment
from flask_login import UserMixin
from models.room import user_room_relationship

class User(Basemodel, Base, UserMixin):
    __tablename__ = 'users'
    name = Column(String(250), nullable=False)
    username = Column(String(250), unique=True)
    email = Column(String(250), unique=True)
    password = Column(String(250), nullable=False)
    address = Column(String(60), nullable=False)
    comments = relationship("Comment", backref="user", cascade="all, delete-orphan")
    rooms = relationship('Room', secondary=user_room_relationship, back_populates='users')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_comments(self):
        from models import storage
        return storage.session.query(Comment).filter(Comment.id == self.id).all()
