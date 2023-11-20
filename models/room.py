from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from models.basemodel import Basemodel, Base
from models.user import User


user_room_relationship = Table('user_room_relationship',
    Column('user_id', String, ForeignKey('user.id')),
    Column('room_id', String, ForeignKey('room.id'))
)


class Room(Basemodel, Base):
    __tablename__ = 'rooms'
    users = relationship('User', secondary=user_room_relationship, back_populates='rooms')