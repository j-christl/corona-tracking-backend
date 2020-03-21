import json


class ResponseBase:
    def __init__(self, success, message=None, payload=None):
        assert isinstance(success, bool)
        if message is None:
            message = str(type(self))
        if payload is None:
            payload = dict()
        self._success = success
        if success:
            self._response_code = 200
        else:
            self._response_code = 500
        self._message = message
        self._payload = payload

    def get_response_code(self):
        return self._response_code

    def get_response_success(self):
        return self._success

    def get_response_message(self):
        return self._message

    def get_response_payload(self):
        return self._payload

    def to_string(self):
        return json.dumps({"success": self._success,
                           "message": self._message,
                           "payload": self._payload})

    response_code = property(get_response_code)
    success = property(get_response_success)
    message = property(get_response_message)
    payload = property(get_response_payload)


class SuccessResponse(ResponseBase):
    def __init__(self, message):
        super().__init__(True, message)


class ErrorResponse(ResponseBase):
    def __init__(self, message):
        super().__init__(False, message)


class CustomResponse(ResponseBase):
    def __init__(self, success, message, **kwargs):
        super().__init__(success=success, message=message, payload=kwargs)
