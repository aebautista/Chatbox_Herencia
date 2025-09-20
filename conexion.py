import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',   # Servidor de MySQL
            user='root',        # Usuario de MySQL
            password='',        # Contraseña
            database='clasesistemas'  # Tu base de datos
        )
        if connection.is_connected():
            print("✅ Conexión exitosa")
    except Error as e:
        print(f"❌ Error al conectar la base de datos: {e}")
    return connection