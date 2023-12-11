'''define wish model'''
from sqlalchemy import Column, String, ForeignKey
from models.basemodel import Basemodel, Base


class Wish(Basemodel, Base):
    '''wish model'''
    __tablename__ = 'wishes'
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(60), ForeignKey("books.id"), nullable=False)
    
    
    def __init__(self, *args, **kwargs):
        '''constructor'''
        super().__init__(*args, **kwargs)