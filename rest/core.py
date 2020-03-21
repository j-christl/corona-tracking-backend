import logging
import time
import jwt

from rest.request import RequestBase, RequestType
from rest.response import CustomResponse, ErrorResponse
from backend.database import Database

logger = logging.getLogger("corona")

SECRET = "supersecretkey"


class RequestProcessor:

    def process_request(self, request):
        assert isinstance(RequestBase)
        request_type = request.request_type
        return getattr(self, "_process_" + request_type.name.lower() + "_request")(request)

    def _process_register_user_request(self, request):
        assert request.request_type is RequestType
        logger.debug("PROCESSING REGISTER USER REQUEST...")
        try:
            user_id = Database.insert_user()
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
        # create json web token
        payload = {
            "userId": user_id,
            "time": int(time.time()),
            "app": "corona_tracker"
        }
        encoded = jwt.encode(payload=payload, key=SECRET, algorithm="HS256")
        return CustomResponse(success=True, message="", userId=user_id, jwt=encoded)
