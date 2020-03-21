import time
from enum import Enum


class RequestType(Enum):
    REGISTER_USER = 0
    UPLOAD_TRACK = 1
    UPDATE_USER_STATUS = 2


class UserStatus(Enum):
    HEALTHY = 0
    INFECTED = 1


class RequestBase:

    def __init__(self, request_type, params):
        assert isinstance(request_type, RequestType)
        assert isinstance(params, dict)

        self._request_type = request_type

    def get_request_type(self):
        return self._request_type

    request_type = property(get_request_type)


class RegisterUserRequest(RequestBase):
    def __init__(self, params):
        super().__init__(RequestType.REGISTER_USER, params)


class UploadTrackRequest(RequestBase):

    def __init__(self, params, body):
        super().__init__(RequestType.UPLOAD_TRACK, params)


class UpdateUserStatusRequest(RequestBase):

    def __init__(self, params):
        super().__init__(RequestType.UPDATE_USER_STATUS, params)