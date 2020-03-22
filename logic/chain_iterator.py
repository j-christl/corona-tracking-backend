import logging
from datetime import datetime, timedelta

from backend.database import Database
from rest.response import ErrorResponse

logger = logging.getLogger("corona")


class ChainIterator:

    @staticmethod
    def process_contact(user_id1, user_id2, relevance_factor):
        logger.info("Processing contact between {} and {} with relevance_factor {}".format(user_id1, user_id2,
                                                                                           relevance_factor))

        risk_level1 = Database.get_users_risk_level(user_id1)
        risk_level2 = Database.get_users_risk_level(user_id2)

        try:
            Database.update_risk_level(user_id2, min(int(risk_level2 + risk_level1 * relevance_factor), 4))
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")

    @staticmethod
    def process_contacts(contact_group):
        for contact in contact_group:
            try:
                if contact[1] > contact[3]:
                    Database.update_risk_level(contact[2], min(int(contact[3] + contact[1] * contact[5]), 4))
                else:
                    Database.update_risk_level(contact[0], min(int(contact[1] + contact[3] * contact[5]), 4))
            except Exception as ex:
                logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
                return ErrorResponse("Database error")

    # Process new contacts with level 5s of the last hour
    @staticmethod
    def process_chains():
        try:
            risk_group = Database.get_users_by_risk_level(5)

            for risk_id in risk_group:
                contact_group = Database.get_contacts_after_timestamp(risk_id[0], datetime.now() - timedelta(hours=1))

                ChainIterator.process_contacts(contact_group)
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
