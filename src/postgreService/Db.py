import psycopg2
from psycopg2 import OperationalError

class Postgres:
    @staticmethod
    def connect():
        host = "1.1.1.1"
        port = "5432"
        database = "database_name"
        user = "user_name"
        password = "password"

        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            connection.autocommit = True
            return connection
        except OperationalError as e:
            print(f"Database connection is unsuccessful: {e}")
            return None



    
        
    
