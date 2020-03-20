import psycopg2
import logging

from config import config


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

    @staticmethod
    def terminate():
        if Database._connection is not None:
            Database._connection.close()
            logger.info("Database connection closed.")

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
            cursor.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error("EXCEPTION DATABASE QUERY {} {}".format(type(e), e))
        finally:
            cursor.close()
        return output
