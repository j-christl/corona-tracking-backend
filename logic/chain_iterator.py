import logging
from datetime import datetime, timedelta

from backend.database import Database
from rest.response import ErrorResponse

logger = logging.getLogger("corona")


class ChainIterator:

    # Process new contacts with level 5s of the last hour
    @staticmethod
    def process_chains():
        try:
            risk_group = Database.get_users_by_risk_level(5)

            for risk_id in risk_group:
                contact_group = Database.get_contacts_after_timestamp(risk_id, datetime.now() - timedelta(hours=1))

                for contact in contact_group:
                    print(contact)
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
