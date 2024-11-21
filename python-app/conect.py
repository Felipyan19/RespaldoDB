import mysql.connector
from pymongo import MongoClient
import pandas as pd

# Función para conectar a MySQL
def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,  
            user="crud_user",  
            password="crudpassword",  
            database="crud_db"  
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL")
            return conexion
    except mysql.connector.Error as e:
        print(f"Error de conexión a MySQL: {e}")
        return None

def conectar_mongo():
    try:
        cliente = MongoClient("mongodb://localhost:27017/")  
        db = cliente["crud_db"]  
        print("Conexión exitosa a MongoDB")
        return db["empleados"]
    except Exception as e:
        print(f"Error de conexión a MongoDB: {e}")
        return None
