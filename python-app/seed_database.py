import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient
import uuid  # Importa la librería para generar un id único

# Generar un id compartido para respaldo
id_respaldo = str(uuid.uuid4())  # Genera un UUID único en formato de cadena

def seed_database_login():
    conexion = None
    try:
        # Conexión a MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            user='crud_user',
            password='crudpassword'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # Crear base de datos
            cursor.execute("CREATE DATABASE IF NOT EXISTS crud_db")
            cursor.execute("USE crud_db")
            
            # Crear tabla de usuarios con id_Respaldo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario VARCHAR(50) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL
                )
            """)
            
            # Eliminar datos existentes
            cursor.execute("DELETE FROM usuarios")
            print("Datos eliminados en usuarios (MySQL).")
            
            # Insertar datos de ejemplo
            usuarios = [
                ( 'admin', 'admin123'),
                ( 'usuario1', 'password123'),
                ( 'usuario2', 'mypassword')
            ]
            
            cursor.executemany(
                "INSERT INTO usuarios ( usuario, contrasena) VALUES (%s, %s)", usuarios
            )
            print("Datos insertados correctamente en Login (MySQL).")

            conexion.commit()
            cursor.close()

    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
            print("Conexión MySQL cerrada.")

def seed_database_mysql(id_respaldo):
    conexion = None
    try:
        # Conexión a MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,  
            user="crud_user",  
            password="crudpassword",  
            database="crud_db",
            connect_timeout=2 
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # Crear tabla de empleados con id_Respaldo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_Respaldo VARCHAR(36) NOT NULL,
                    nombre VARCHAR(50) NOT NULL UNIQUE,
                    numero_identidad VARCHAR(20) NOT NULL UNIQUE,
                    tipo_identidad VARCHAR(20) NOT NULL,
                    direccion VARCHAR(100),
                    foto LONGTEXT,
                    cargo VARCHAR(50),
                    hv LONGTEXT
                )
            """)
            
            # Eliminar datos existentes
            cursor.execute("DELETE FROM empleados")
            print("Datos eliminados en empleados (MySQL).")
            
            # Insertar datos de ejemplo
            empleados = [
                (id_respaldo, 'Pedro', '123456789', 'CC', 'Calle 123', None, 'Gerente', None),
            ]
            
            cursor.executemany(
                "INSERT INTO empleados (id_Respaldo, nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", empleados
            )
            print("Datos insertados correctamente en empleados (MySQL).")

            conexion.commit()
            cursor.close()

    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
            print("Conexión MySQL cerrada.")

def seed_database_mongo(id_respaldo):
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb://localhost:27017/',serverSelectionTimeoutMS=2000)
        db = client['crud_db']

        # Crear colección de empleados
        empleados = db['empleados']
        
        # Eliminar documentos existentes
        empleados.delete_many({})
        print("Datos eliminados en empleados (MongoDB).")

        # Insertar datos de ejemplo en la colección 'empleados'
        empleados_data = [
            {'id_Respaldo': id_respaldo, 'nombre': 'Pedro', 'numero_identidad': '123456789', 'tipo_identidad': 'CC', 'direccion': 'Calle 123', 'foto': None, 'cargo': 'Gerente', 'hv': None}
        ]
        
        empleados.insert_many(empleados_data)
        print("Datos insertados correctamente en empleados (MongoDB).")

        client.close()

    except Exception as e:
        print(f"Error al conectar a la base de datos MongoDB: {e}")
    finally:
        print("Conexión MongoDB cerrada.")

if __name__ == "__main__":
    seed_database_login()
    seed_database_mysql(id_respaldo)
    seed_database_mongo(id_respaldo)
