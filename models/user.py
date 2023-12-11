'''define user, and room models'''
from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
from models.basemodel import Basemodel, Base
from models.comment import Comment
from flask_login import UserMixin

#user_room_relationship table
user_room_relationship = Table('user_room_relationship', Base.metadata,
    Column('user_id', String(60), ForeignKey('users.id')),
    Column('room_id', String(60), ForeignKey('rooms.id'))
)

class Room(Basemodel, Base):
    '''room model'''
    __tablename__ = 'rooms'
    users = relationship('User', secondary=user_room_relationship, back_populates='rooms')
    messages = relationship("Message", backref="room", cascade="all, delete-orphan")
    members = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        '''constructor'''
        super().__init__(*args, **kwargs)


class User(Basemodel, Base, UserMixin):
    '''user model'''
    __tablename__ = 'users'
    name = Column(String(250), nullable=False)
    username = Column(String(250), unique=True)
    email = Column(String(250), unique=True)
    password = Column(String(250), nullable=False)
    address = Column(String(60), nullable=False)
    comments = relationship("Comment", backref="user", cascade="all, delete-orphan")
    wishes = relationship("Wish", backref="user", cascade="all, delete-orphan")
    offers = relationship("Offer", backref="user", cascade="all, delete-orphan")
    rooms = relationship('Room', secondary=user_room_relationship, back_populates='users')
    
    def __init__(self, *args, **kwargs):
        '''constructor'''
        super().__init__(*args, **kwargs)

    def get_comments(self):
        '''get comments made by user'''
        from models import storage
        return storage.session.query(Comment).filter(Comment.id == self.id).all()
