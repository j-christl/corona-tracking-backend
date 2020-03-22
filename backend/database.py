import logging

import psycopg2

from cfg.config import config

logger = logging.getLogger("corona")


class Database:
    _connection = None

    @staticmethod
    def initialize():
        try:
            params = config("postgresql")
            logger.info('Connecting to the PostgreSQL database...')
            Database._connection = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as e:
            logger.error("EXCEPTION INITIALIZING DATABASE {} {}".format(type(e), e))
            return False
        return True

    @staticmethod
    def terminate():
        if Database._connection is not None:
            Database._connection.close()
            logger.info("Database connection closed.")

    @staticmethod
    def insert_user():
        logger.info("INSERTING USER...")
        cursor = Database._connection.cursor()
        cursor.callproc("insert_user")
        user_id = cursor.fetchone()[0]
        Database._connection.commit()
        logger.info("GENERATED USER ID: {}".format(user_id))
        cursor.close()
        return user_id

    @staticmethod
    def update_risk_level(user_id, level):
        logger.info("Updating level of user " + str(user_id) + " to " + str(level))
        cursor = Database._connection.cursor()
        cursor.callproc("update_risk_level", (user_id, level))
        Database._connection.commit()
        cursor.close()

    @staticmethod
    def insert_infected(user_id, firstname, lastname, phonenumber):
        logger.info("Inserting infected user " + str(user_id))
        cursor = Database._connection.cursor()
        cursor.callproc("insert_infected", (user_id, firstname, lastname, phonenumber))
        Database._connection.commit()
        cursor.close()

    @staticmethod
    def report_contact(reporting_user, contacted_user, contact_time, relevance_factor):
        cursor = Database._connection.cursor()
        logger.debug(
            "EXECUTING DB FUNC: report_contact({}, {}, {}, {})".format(reporting_user, contacted_user, contact_time,
                                                                       relevance_factor))
        cursor.callproc("report_contact", (reporting_user, contacted_user, contact_time, relevance_factor))
        Database._connection.commit()
        cursor.close()

    @staticmethod
    def get_users_by_risk_level(risk_level):
        logger.info("Getting users by risk level {}".format(risk_level))
        cursor = Database._connection.cursor()
        cursor.callproc("get_users_by_risk_level", (risk_level,))
        Database._connection.commit()
        users = cursor.fetchall()
        cursor.close()
        return users

    @staticmethod
    def get_contacts_after_timestamp(user_id, time_thresh):
        logger.info("Getting contacts after timestamp for user {}, time_thresh {}".format(user_id, time_thresh))
        cursor = Database._connection.cursor()
        cursor.callproc("get_contacts_after_timestamp", (user_id, time_thresh))
        Database._connection.commit()
        contacted_users = cursor.fetchall()
        cursor.close()
        return contacted_users

    @staticmethod
    def insert_geo_data(user_id, lat, lon, gps_time):
        logger.info(
            "Inserting geo data for user_id {}, lat {}, lon {}, grp_time {}".format(user_id, lat, lon, gps_time))
        cursor = Database._connection.cursor()
        cursor.callproc("insert_geo_data", (user_id, lat, lon, gps_time))
        Database._connection.commit()
        cursor.close()

    @staticmethod
    def get_geo_data_after_timestamp(user_id, time_thresh):
        logger.info("Getting geo data after timestamp for user_id {}, time_thresh {}".format(user_id, time_thresh))
        cursor = Database._connection.cursor()
        cursor.callproc("get_geo_data_after_timestamp", (user_id, time_thresh))
        Database._connection.commit()
        geo_data = cursor.fetchall()
        cursor.close()
        return geo_data

    @staticmethod
    def get_users_risk_level(user_id):
        logger.info("Getting users risk level for user_id {}".format(user_id))
        cursor = Database._connection.cursor()
        cursor.callproc("get_users_risk_level", (user_id,))
        Database._connection.commit()
        risk_level = cursor.fetchone()[0]
        cursor.close()
        return risk_level

    @staticmethod
    def get_users_below_risk_level(risk_level):
        logger.info("Getting users below risk_level {}".format(risk_level))
        cursor = Database._connection.cursor()
        cursor.callproc("get_users_below_risk_level", (risk_level,))
        Database._connection.commit()
        users = cursor.fetchall()
        cursor.close()
        return users

    @staticmethod
    def execute_query(query):
        """ Execute a SQL query """
        assert isinstance(query, str)
        logger.info("Executing SQL query:\n" + query)
        cursor = Database._connection.cursor()
        cursor.execute(query)
        output = None
        try:
            cursor = Database._connection.cursor()
            cursor.execute(query)
            output = cursor.fetchmany()
            Database._connection.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error("EXCEPTION DATABASE QUERY {} {}".format(type(e), e))
        finally:
            cursor.close()
        return output
