from database.db_connection import get_connection

connection = get_connection()

print("Database connection successful!")

connection.close()