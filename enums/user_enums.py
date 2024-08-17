from enum import Enum

class UserStatus(Enum):
    Declined = -1
    Pending = 0
    Accepted = 1