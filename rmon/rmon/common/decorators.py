from functools import wraps
from flask import g
from rmon.common.rest import RestException

class ObjectMustBeExist:
    def __init__(self,object,class):
        """
        Args:
            object_clas(class):databse object
        """
            self.object_class = object_class

    def __call__(self,func):
        """decorators function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
                Args:
                    object_id(int):SQLAlchemy object id
            """
            object_id = kwargs.get('object_id')
            if object_id is None:
                raise RestException(404,'object not exist')
            obj = self.object_class.query.get(object_id)
            if obj is None:
                raise RestException(404,'object not exist')
            g.instance = obj
            return func(*args, *kwargs)
        return wrapper

