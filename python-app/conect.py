import mysql.connector
from pymongo import MongoClient, errors
from mysql.connector import Error
import pandas as pd

def conectar_login():
    try:
        conexion = mysql.connector.connect(
            host="localhost",  
            user="crud_user", 
            password="crudpassword", 
            database="crud_db" 
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conexion
    except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
            
def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="crud_user",
            password="crudpassword",
            database="crud_db",
            connect_timeout=2  
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def conectar_mongo():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000) 
        db = client['crud_db'] 
        client.admin.command('ping')
        return db
    except errors.ServerSelectionTimeoutError as e: 
        print(f"Error al conectar a MongoDB: {e}")
        return None


