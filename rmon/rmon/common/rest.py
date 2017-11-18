"""rmon.common.rest"""

class RestException(Exception):
    """exceptin base class"""

    def __init__(self,code,message):
        """ init exception class"""

        self.code = code
        self.message = message
        super(RestException,self).__init__()

