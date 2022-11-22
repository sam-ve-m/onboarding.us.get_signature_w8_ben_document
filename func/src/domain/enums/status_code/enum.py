# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    INTERNAL_SERVER_ERROR = 100
    RESPONSE_ERROR_DRIVE_WEALTH = 50
    WAS_NOT_SENT_TO_PERSEPHONE = 60
    USER_WAS_NOT_FOUND = 69
    TRANSPORT_ON_BOARDING_ERROR = 88
    NOT_DATE_TIME = 99

    def __repr__(self):
        return self.value
