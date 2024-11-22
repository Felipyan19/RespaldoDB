import mysql.connector
from mysql.connector import Error

def seed_database():
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
                print("Datos insertados correctamente.")
            else:
                print("La base de datos ya contiene datos.")

            conexion.commit()
            cursor.close()

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    seed_database()
