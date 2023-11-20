from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class Basemodel:
    id = Column(String(60), primary_key=True, nullable=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())

    def save(self):
        from models import storage
        storage.new(self)
        storage.save()

    def __str__(self):
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         new_dict)

    def to_dict(self, save_fs=None):
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        new_dict.pop("_sa_instance_state", None)
        return new_dict
