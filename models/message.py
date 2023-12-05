from sqlalchemy import Column, String, ForeignKey, DateTime
from models.basemodel import Basemodel, Base



class Message(Basemodel, Base):
    __tablename__ = 'messages'
    text = Column(String(1000), nullable=False)
    date = Column(DateTime)
    name = Column(String(250), nullable=False)
    room_id = Column(String(60), ForeignKey("rooms.id"), nullable=False)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)