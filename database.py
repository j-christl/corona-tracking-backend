import psycopg2
import logging

from config import config


logger = logging.getLogger("corona")


class Database:
    _connection = None

    _create_table_commands = (
        """
        CREATE TABLE "vendors" (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE "parts" (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE "part_drawings" (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS "vendor_parts" (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)

    @staticmethod
    def initialize():
        try:
            params = config("postgresql")
            logger.info('Connecting to the PostgreSQL database...')
            Database._connection = psycopg2.connect(**params)

            # create tables
            cursor = Database._connection.cursor()
            for command in Database._create_table_commands:
                cursor.execute(command)

            cursor.close()
            Database._connection.commit()

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
