import logging
from datetime import datetime, timedelta
from math import sin, cos, atan2, sqrt

from backend.database import Database
from logic.chain_iterator import ChainIterator
from rest.response import ErrorResponse

logger = logging.getLogger("corona")


class GeoProcessor:

    @staticmethod
    def calculate_distance(geo_data1, geo_data2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = geo_data1[0]
        lon1 = geo_data1[1]
        lat2 = geo_data2[0]
        lon2 = geo_data2[1]

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c * 1000

        return distance

    @staticmethod
    def identify_contacts(risk_id, geo_data, geo_data_subject):
        for coordinate in geo_data:
            coord_time = datetime.strptime(coordinate[3], '%Y-%m-%d %H:%M:%S.%f')

            for coordinate_subject in geo_data_subject:
                subject_time = datetime.strptime(coordinate_subject[3], '%Y-%m-%d %H:%M:%S.%f')
                if (coord_time - subject_time) < timedelta(seconds=5):
                    if GeoProcessor.calculate_distance(coordinate, coordinate_subject) <= 1:
                        logger.info("Contact detected between {} and {}".format(risk_id, coordinate_subject[0]))
                        ChainIterator.process_contact(risk_id, coordinate_subject[0], 0.5)

    @staticmethod
    def iterate_geo_data():
        logger.info("Iterating geo data")

        risk_group = Database.get_users_by_risk_level(5)

        try:
            for risk_id in risk_group:
                geo_data = Database.get_geo_data_after_timestamp(risk_id, datetime.now() - timedelta(hours=1))
                contact_subjects = Database.get_users_below_risk_level(4)

                for subject in contact_subjects:
                    geo_data_subject = Database.get_geo_data_after_timestamp(subject[0],
                                                                             datetime.now() - timedelta(hours=1))
                    GeoProcessor.identify_contacts(risk_id, geo_data, geo_data_subject)
        except Exception as ex:
            logger.error("EXCEPTION DATABASE: {} {}".format(type(ex), ex))
            return ErrorResponse("Database error")
