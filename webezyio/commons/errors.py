class WebezyCoderError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        error -- Which error type
        message -- explanation of the error
    """

    def __init__(self, error, message="Unknown webezy error"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.error}] {self.message}'


class WebezyProtoError(Exception):
    """Exception raised for errors in the proto parse process.

    Attributes:
        resource -- Which resource the error is triggered on
        message -- explanation of the error
    """

    def __init__(self, resource, message="Error occured during parsing of proto file"):
        self.resource = resource
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.resource}] {self.message}'


class WebezyValidationError(Exception):

    def __init__(self, resource, message="Error occured during parsing of proto type"):
        self.resource = resource
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.resource}] {self.message}'
