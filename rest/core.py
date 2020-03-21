import logging
import time
import jwt

from rest.request import RequestBase, RequestType, UploadTrackRequest, UpdateUserStatusRequest
from rest.response import CustomResponse, ErrorResponse, SuccessResponse
from backend.database import Database
from cfg.config import config

logger = logging.getLogger("corona")


class RequestProcessor:

    def process_request(self, request):
        assert isinstance(request, RequestBase)
        request_type = request.request_type
        return getattr(self, "_process_" + request_type.name.lower() + "_request")(request)

    def _process_register_user_request(self, request):
        assert request.request_type is RequestType.REGISTER_USER
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
        params = config("auth")
        secret = params["jwtsecret"]
        encoded = jwt.encode(payload=payload, key=secret, algorithm="HS256").decode("utf-8")
        return CustomResponse(success=True, message="", userId=user_id, jwt=encoded)


    def _process_upload_track_request(self, request):
        assert isinstance(request, UploadTrackRequest)
        logger.debug("PROCESSING UPLOAD TRACK REQUEST...")

        contacts = request.contacts
        postions = request.positions
        try:
            # TODO: insert into database
            pass
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
        return SuccessResponse("Upload succeeded")

    def _process_update_user_status_request(self, request):
        assert isinstance(request, UpdateUserStatusRequest)
        logger.debug("PROCESSING UPDATE USER STATUS request")

        user_id = request.user_id
        new_user_status = request.new_user_status
        try:
            # TODO: update database
            pass
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
        return SuccessResponse("Status update succeeded")
