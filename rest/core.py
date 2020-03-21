import jwt

from rest.request import RequestBase, RequestType
from rest.response import CustomResponse

class RequestProcessor:

    def process_request(self, request):
        assert isinstance(RequestBase)
        request_type = request.request_type
        return getattr(self, "_process_" + request_type.name.lower() + "_request")(request)

    def _process_register_user_request(self, request):
        assert request.request_type is RequestType
        logger.debug("PROCESSING ORDER BOOK REQUEST...")

        # create json web token
        user_id = None
        jwt = None
        return CustomResponse(success=true, message="", userId=user_id, jwt=jwt)
