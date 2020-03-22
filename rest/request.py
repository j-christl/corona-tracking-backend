import logging
from datetime import datetime
from enum import Enum

import jwt

from cfg.config import config

logger = logging.getLogger("corona")


class RequestType(Enum):
    REGISTER_USER = 0
    UPLOAD_TRACK = 1
    UPDATE_USER_STATUS = 2
    GET_USER_STATUS = 3
    UPLOAD_PERSONAL_DATA = 4


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
        secret = secret.encode("utf-8")
        self._jwt = jwt.decode(params["jwt"], secret,  algorithms=["HS256"])  # throws exeption if validation fails
        logger.debug("DECODED JWT: {}".format(self._jwt))


class UploadTrackRequest(AuthRequestBase):

    def __init__(self, params, body):
        super().__init__(RequestType.UPLOAD_TRACK, params)

        if body is None:
            raise ValueError("Missing request body")
        if "contacts" not in body:
            raise ValueError("Missing body data: contacts")
        if "positions" not in body:
            raise ValueError("Missing body data: positions")

        self._user_id = self._jwt["userId"]

        # relevance factor for direct contacts is always 1
        self._contacts = [(self._jwt["userId"],) + (i[0], datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S.%f')) + (1,) for i in body["contacts"]]
        logger.debug("GOT CONTACTS DATA: {}".format(self._contacts))
        self._positions = [(j[0], j[1], datetime.strptime(j[2], '%Y-%m-%d %H:%M:%S.%f')) for j in body["positions"]]
        logger.debug("GOT POSITIONS DATA: {}".format(self._positions))

    def get_user_id(self):
        return self._user_id

    def get_contacts(self):
        return self._contacts

    def get_positions(self):
        return self._positions

    user_id = property(get_user_id)
    contacts = property(get_contacts)
    positions = property(get_positions)


class UpdateUserStatusRequest(AuthRequestBase):

    def __init__(self, params):
        super().__init__(RequestType.UPDATE_USER_STATUS, params)

        if "status" not in params:
            raise ValueError("Missing request parameter: status")
        status = params["status"]
        self._user_id = self._jwt["userId"]
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


class GetUserStatusRequest(AuthRequestBase):

    def __init__(self, params):
        super().__init__(RequestType.GET_USER_STATUS, params)

        self._user_id = self._jwt["userId"]

    def get_user_id(self):
        return self._user_id

    user_id = property(get_user_id)


class UploadPersonalDataRequest(AuthRequestBase):

    def __init__(self, params):
        super().__init__(RequestType.UPLOAD_PERSONAL_DATA, params)

        if "firstname" not in params:
            raise ValueError("Missing request parameter: firstname")
        if "lastname" not in params:
            raise ValueError("Missing request parameter: lastname")
        if "phonenumber" not in params:
            raise ValueError("Missing request parameter: phonenumber")

        self._firstname = params["firstname"]
        self._lastname = params["lastname"]
        self._phonenumber = params["phonenumber"]

        self._user_id = self._jwt["userId"]

    def get_user_id(self):
        return self._user_id

    def get_firstname(self):
        return self._firstname

    def get_lastname(self):
        return self._lastname

    def get_phonenumber(self):
        return self._phonenumber

    user_id = property(get_user_id)
    firstname = property(get_firstname)
    lastname = property(get_lastname)
    phonenumber = property(get_phonenumber)
