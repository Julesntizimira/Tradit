from sqlalchemy import Column, String, ForeignKey
from models.basemodel import Basemodel, Base


class Wish(Basemodel, Base):
    __tablename__ = 'wishes'
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    book_id = Column(String(60), ForeignKey("books.id"), nullable=False)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)