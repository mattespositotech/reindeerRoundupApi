class NoValidCombinationError(Exception):
    """Exception raised when no valid combination of values can be found."""
    def __init__(self, message="No valid combination of values can be found."):
        self.message = message
        super().__init__(self.message)