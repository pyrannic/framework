class IllegalArgumentException(ValueError):
    """
    Exception raised when an illegal argument is passed to a function or method.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = "Illegal argument provided."):
        self.message = message
        super().__init__(self.message)
