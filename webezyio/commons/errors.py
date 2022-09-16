class WebezyCoderError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        error -- Which error type
        message -- explanation of the error
    """

    def __init__(self, error, message="Unknown webezy error"):
        self.salary = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.error}] {self.message}'