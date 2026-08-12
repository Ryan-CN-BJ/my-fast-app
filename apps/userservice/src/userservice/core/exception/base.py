class BaseException(Exception):
    def __init__(self, message: str, *, original_exception: Exception | None = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(message)
