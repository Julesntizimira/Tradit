from models.user import User, Base, Basemodel, Room
from models.comment import Comment
from models.book import Book
from models.genre import Genre
from models.author import Author
from models.message import Message
from models.wish import Wish
from models.offer import Offer 
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


classes = {
    'User': User,
    'Book': Book,
    'Genre': Genre,
    'Author': Author,
    'Comment': Comment,
    'Room': Room,
    'Message': Message,
    'Offer': Offer,
    'Wish': Wish
    }


class Dbmanager:
    __engine = None
    __session = None
    def __init__(self):
        self.__engine = create_engine('mysql+mysqlconnector://jules:mypassword@localhost:3306/bookdb', isolation_level='READ COMMITTED')

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
       
    def save(self):
        self.__session.commit()

    def new(self, obj):
         self.__session.add(obj)

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        Base.metadata.create_all(bind=self.__engine)
        SessionFactory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        ScopedSessionFactory = scoped_session(SessionFactory)
        self.__session = ScopedSessionFactory() 

    def close(self):
        self.__session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None
        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()
        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())
        return count
    
    @property
    def session(self):
        return self.__session