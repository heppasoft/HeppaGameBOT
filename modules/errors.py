class BaseError(Exception): pass

class InvalidCommandChannel(BaseError): pass

class UnknownUser(BaseError): pass