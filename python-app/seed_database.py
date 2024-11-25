import mysql.connector
from mysql.connector import Error
from pymongo import MongoClient

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
            
            # Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario VARCHAR(50) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL
                )
            """)
            
            # Insertar datos de ejemplo
            usuarios = [
                ('admin', 'admin123'),
                ('usuario1', 'password123'),
                ('usuario2', 'mypassword')
            ]
            
            # Insertar datos si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)", usuarios
                )
                print("Datos insertados correctamente en Login (MySQL).")
            else:
                print("La base de datos ya contiene datos en Login (MySQL).")

            conexion.commit()
            cursor.close()

    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
            print("Conexión MySQL cerrada.")

def seed_database_mysql():
    conexion = None
    try:
        # Conexión a MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,  
            user="crud_user",  
            password="crudpassword",  
            database="crud_db"  
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # Crear tabla de empleados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL UNIQUE,
                    numero_identidad VARCHAR(20) NOT NULL UNIQUE,
                    tipo_identidad VARCHAR(20) NOT NULL,
                    direccion VARCHAR(100),
                    foto LONGTEXT,
                    cargo VARCHAR(50),
                    hv LONGTEXT
                )
            """)
            
            # Insertar datos de ejemplo
            empleados = [
                ('Pedro', '123456789', 'CC', 'Calle 123', None, 'Gerente', None),
            ]
            
            # Insertar datos si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM empleados")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO empleados (nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv) VALUES (%s, %s, %s, %s, %s, %s, %s)", empleados
                )
                print("Datos insertados correctamente en empleados (MySQL).")
            else:
                print("La base de datos ya contiene datos en empleados (MySQL).")

            conexion.commit()
            cursor.close()

    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
            print("Conexión MySQL cerrada.")

def seed_database_mongo():
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['crud_db']

        # Crear colección de usuarios
        empleados = db['empleados']


        # Insertar datos de ejemplo en la colección 'empleados'
        empleados_data = [
            {'nombre': 'Pedro', 'numero_identidad': '123456789', 'tipo_identidad': 'CC', 'direccion': 'Calle 123', 'foto': None, 'cargo': 'Gerente', 'hv': None}
        ]

        if empleados.count_documents({}) == 0:
            empleados.insert_many(empleados_data)
            print("Datos insertados correctamente en empleados (MongoDB).")
        else:
            print("La base de datos ya contiene datos en empleados (MongoDB).")

        client.close()

    except Exception as e:
        print(f"Error al conectar a la base de datos MongoDB: {e}")
    finally:
        print("Conexión MongoDB cerrada.")

if __name__ == "__main__":
    seed_database_login()
    seed_database_mysql()
    seed_database_mongo()
