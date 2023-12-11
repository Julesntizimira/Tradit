'''define Basemodel class'''
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class Basemodel:
    '''Base class to define common methods and behaviours shared with all Models'''
    id = Column(String(60), primary_key=True, nullable=True)

    def __init__(self, *args, **kwargs):
        '''constructor'''
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())

    def save(self):
        '''save the instance to storage'''
        from models import storage
        storage.new(self)
        storage.save()

    def __str__(self):
        '''return string represantation of an instance'''
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         new_dict)

    def to_dict(self, save_fs=None):
        '''return dictionary represantation of an instance'''
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        new_dict.pop("_sa_instance_state", None)
        result = {}
        for key, value in new_dict.items():
            if not isinstance(value, (list, Base)):
                result[key] = value
        return result
