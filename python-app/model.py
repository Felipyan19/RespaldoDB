from pymongo import MongoClient
import mysql.connector
from mysql.connector import Error
import uuid
import pandas as pd

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
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def conectar_mongo():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['crud_db']
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

def fetch_data():
    try:
        mysql_db = conectar_mysql()
        query = "SELECT * FROM empleados"
        df_mysql = pd.read_sql(query, mysql_db)
        print("Datos MySQL:", df_mysql)
        mysql_db.close()
    except Exception as e:
        print(f"Error al obtener datos de MySQL: {e}")
        df_mysql = pd.DataFrame()

    try:
        db = conectar_mongo()
        empleados = db['empleados']
        df_mongo = pd.DataFrame(list(empleados.find({})))
        print("Datos MongoDB:", df_mongo)
    except Exception as e:
        print(f"Error al obtener datos de MongoDB: {e}")
        df_mongo = pd.DataFrame()

    # Limpieza de datos y combinación
    if not df_mysql.empty:
        df_mysql = df_mysql.drop(columns=['id'])
    if not df_mongo.empty:
        df_mongo = df_mongo.drop(columns=['_id'])
    
    df_final = pd.concat([df_mysql, df_mongo]).drop_duplicates().reset_index(drop=True)
    return df_final

def insert_data(record):
    responses = []

    # Generar id_Respaldo único
    id_respaldo = str(uuid.uuid4())
    record["id_Respaldo"] = id_respaldo

    # Insertar en MySQL
    try:
        mysql_db = conectar_mysql()
        cursor = mysql_db.cursor()
        query = """
            INSERT INTO empleados (id_Respaldo, nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            record["id_Respaldo"],
            record["nombre"],
            record["numero_identidad"],
            record["tipo_identidad"],
            record["direccion"],
            record["foto"],
            record["cargo"],
            record["hv"]
        )
        cursor.execute(query, values)
        mysql_db.commit()
        responses.append("Registro guardado en MySQL")
    except Exception as e:
        mysql_db.rollback()
        responses.append(f"Error en MySQL: {e}")
    finally:
        cursor.close()
        mysql_db.close()

    # Insertar en MongoDB
    try:
        db = conectar_mongo()
        empleados_collection = db['empleados']
        empleados_collection.insert_one(record)
        responses.append("Registro guardado en MongoDB")
    except Exception as e:
        responses.append(f"Error en MongoDB: {e}")

    return responses

def update_data(record):
    responses = []

    try:
        mysql_db = conectar_mysql()
        cursor = mysql_db.cursor()
        query = """
            UPDATE empleados
            SET id_Respaldo = %s, nombre = %s, tipo_identidad = %s, direccion = %s, foto = %s, cargo = %s, hv = %s
            WHERE numero_identidad = %s
        """
        values = (
            record["id_Respaldo"],
            record["nombre"],
            record["tipo_identidad"],
            record["direccion"],
            record["foto"],
            record["cargo"],
            record["hv"],
            record["numero_identidad"]
        )
        cursor.execute(query, values)
        mysql_db.commit()
        responses.append("Registro actualizado en MySQL")
    except Exception as e:
        mysql_db.rollback()
        responses.append(f"Error en MySQL: {e}")
    finally:
        cursor.close()
        mysql_db.close()

    # Actualizar en MongoDB
    try:
        db = conectar_mongo()
        empleados = db['empleados']
        empleados.update_one(
            {"id_Respaldo": record["id_Respaldo"]},
            {"$set": record}
        )
        responses.append("Registro actualizado en MongoDB")
    except Exception as e:
        responses.append(f"Error en MongoDB: {e}")

    title = "Actualización Completa" if all("actualizado" in msg for msg in responses) else "Error en Actualización"
    message = "; ".join(responses)
    
    return title, message
