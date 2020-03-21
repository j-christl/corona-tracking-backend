import time
from enum import Enum
import jwt
import logging

from cfg.config import config

logger = logging.getLogger("corona")


class RequestType(Enum):
    REGISTER_USER = 0
    UPLOAD_TRACK = 1
    UPDATE_USER_STATUS = 2


class UserStatus(Enum):
    HEALTHY = 0
    INFECTED = 1


class RequestBase:

    def __init__(self, request_type):
        assert isinstance(request_type, RequestType)
        self._request_type = request_type

    def get_request_type(self):
        return self._request_type

    request_type = property(get_request_type)


class RegisterUserRequest(RequestBase):
    def __init__(self, params):
        super().__init__(RequestType.REGISTER_USER)


class AuthRequestBase(RequestBase):

    def __init__(self, request_type, params):
        assert isinstance(params, dict)
        super().__init__(request_type)

        if "jwt" not in params:
            raise ValueError("Missing request parameter: jwt")
        secret = config("auth")["jwtsecret"]
        decoded = jwt.decode(params["jwt"], secret,  algorithms=["HS256"])  # throws exeption if validation fails
        logger.debug("DECODED JWT: {}".format(decoded))


class UploadTrackRequest(AuthRequestBase):

    def __init__(self, params, body):
        super().__init__(RequestType.UPLOAD_TRACK, params)

        if body is None:
            raise ValueError("Missing request body")


class UpdateUserStatusRequest(AuthRequestBase):

    def __init__(self, params):
        super().__init__(RequestType.UPDATE_USER_STATUS, params)

        if "userId" not in params:
            raise ValueError("Missing request parameter: userId")
        self._user_id = params["userId"]
        if "status" not in params:
            raise ValueError("Missing request parameter: status")
        status = params["status"]
        try:
            self._new_user_status = UserStatus[status]
        except Exception as e:
            raise ValueError("Invalid request parameter value: status = " + status)

    def get_user_id(self):
        return self._user_id

    def get_new_user_status(self):
        return self._new_user_status

    user_id = property(get_user_id)
    new_user_status = property(get_new_user_status)

