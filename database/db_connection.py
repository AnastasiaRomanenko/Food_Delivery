import psycopg2
from typing import Optional

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = psycopg2.connect(
                dbname="food_delivery",
                user="postgres",
                password="your_password_here",  # Replace with your actual password
                host="localhost",
                port="5432"
            )
        return cls._instance


    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            return results
        else:
            self.connection.commit()
    
    def execute_query_returning_id(self, query, params):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            user_id = cursor.fetchone()[0]
            self.connection.commit()
        return user_id

    def close(self):
        if self.connection:
            self.connection.close() 