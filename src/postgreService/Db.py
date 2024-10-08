import psycopg2
from psycopg2 import OperationalError

class Postgres:
    @staticmethod
    def connect():
        host = "185.148.240.19"
        port = "5432"
        database = "KlemsanIOT"
        user = "KlemsanIOTUserLimited"
        password = "1234klemsan4321"

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



    
        
    