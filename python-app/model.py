import sys
import time
import datetime
import mysql.connector
from pymongo import MongoClient, errors
import uuid
import pandas as pd
from mysql.connector import Error
from conect import conectar_mysql, conectar_mongo

failed_records = pd.DataFrame(columns=["id_Respaldo", "nombre", "numero_identidad", "tipo_identidad", "direccion", "foto", "cargo", "hv", "error"])

def fetch_data():
    try:
        mysql_db = conectar_mysql()
        if mysql_db is not None:
            query = "SELECT * FROM empleados"
            df_mysql = pd.read_sql(query, mysql_db)
            print("Datos MySQL:", df_mysql)
            mysql_db.close()
        else:
            df_mysql = pd.DataFrame()
            print("No se pudo conectar a MySQL para obtener datos.")
    except Exception as e:
        print(f"Error al obtener datos de MySQL: {e}")
        df_mysql = pd.DataFrame()

    try:
        db = conectar_mongo()
        if db is not None: 
            empleados = db['empleados']
            df_mongo = pd.DataFrame(list(empleados.find({})))
            print("Datos MongoDB:", df_mongo)
        else:
            df_mongo = pd.DataFrame()
            print("No se pudo conectar a MongoDB para obtener datos.")
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

def insert_data(record, database=None):
    global failed_records
    responses = []

    if record["id_Respaldo"] is None or record["id_Respaldo"] == "":
        id_respaldo = str(uuid.uuid4())
        record["id_Respaldo"] = id_respaldo

    if database is None or database == "mysql":
    
        mysql_db = conectar_mysql()
        if mysql_db is None:
            record_with_error = {**record, "error": "Insertar - MySQL"}
            failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
            responses.append("No se pudo conectar a MySQL")
        else:
            try:
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
                print("Registro guardado en MySQL")
                responses.append("Registro guardado en MySQL")
            except Exception as e:
                mysql_db.rollback()

                record_with_error = {**record, "error": "Insertar - MySQL"}
                failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
                responses.append(f"Error en MySQL: {e}")
            finally:
                cursor.close()
                mysql_db.close()

    if database is None or database == "mongodb":
        
        try:
            db = conectar_mongo()
            if db is not None:
                empleados_collection = db['empleados']
                empleados_collection.insert_one(record)
                print("Registro guardado en MongoDB")
                responses.append("Registro guardado en MongoDB")
            else:
                record_with_error = {**record, "error": "Insertar - MongoDB"}
                failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
                responses.append("Error en MongoDB: No se pudo conectar a MongoDB")
        except Exception as e:
            record_with_error = {**record, "error": "Insertar - MongoDB"}
            failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)

            responses.append(f"Error en MongoDB: {e}")

    return responses

def update_data(record, database=None):
    global failed_records  
    responses = []

    if database is None or database == "mysql":
        try:
            mysql_db = conectar_mysql()
            if mysql_db is not None:
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
                print("Registro actualizado en MySQL")
                responses.append("Registro actualizado en MySQL")
            else:
                record_with_error = {**record, "error": "Actualizar - MySQL"}
                failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
                responses.append("Error al conectar a MySQL para actualizar.")
        except Exception as e:
            if mysql_db:
                mysql_db.rollback()
            record_with_error = {**record, "error": "Actualizar - MySQL"}
            failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
            responses.append(f"Error en MySQL: {e}")
        finally:
            if mysql_db:
                cursor.close()
                mysql_db.close()
    if database is None or database == "mongodb":
        try:
            db = conectar_mongo()
            if db is not None:
                empleados = db['empleados']
                empleados.update_one(
                    {"id_Respaldo": record["id_Respaldo"]},
                    {"$set": record}
                )
                print("Registro actualizado en MongoDB")
                responses.append("Registro actualizado en MongoDB")
            else:
                record_with_error = {**record, "error": "Actualizar - MongoDB"}
                failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
                responses.append("Error al conectar a MongoDB para actualizar.")
        except Exception as e:
            record_with_error = {**record, "error": "Actualizar - MongoDB"}
            failed_records = pd.concat([failed_records, pd.DataFrame([record_with_error])], ignore_index=True)
            responses.append(f"Error en MongoDB: {e}")

        title = "Actualización Completa" if all("actualizado" in msg for msg in responses) else "Error en Actualización"
        message = "; ".join(responses)
    
    return title, message

def procesar_registros_mysql():
    global failed_records

    resultado_mysql = failed_records[failed_records['error'].str.contains("MySQL", na=False)]
    if not resultado_mysql.empty:
        print("Procesando registros fallidos en MySQL...")

        mysql_db = conectar_mysql()
        if mysql_db is None:
            print("No se pudo conectar a MySQL.")
            return
        mysql_db.close()
        for index, row in resultado_mysql.iterrows():
            id_respaldo = row['id_Respaldo']
            record = {
                "id_Respaldo": id_respaldo,
                "nombre": row['nombre'],
                "numero_identidad": row['numero_identidad'],
                "tipo_identidad": row['tipo_identidad'],
                "direccion": row['direccion'],
                "foto": row['foto'],
                "cargo": row['cargo'],
                "hv": row['hv']
            }

            if row['error'] == "Insertar - MySQL":
                print("Insertando registro en MySQL...")
                insert_data(record, "mysql")
            elif row['error'] == "Actualizar - MySQL":
                print("Actualizando registro en MySQL...")
                update_data(record, "mysql")
        
        failed_records = failed_records[~failed_records['error'].str.contains("MySQL", na=False)]

def procesar_registros_mongo():
    global failed_records

    resultado_mongo = failed_records[failed_records['error'].str.contains("MongoDB", na=False)]
    if not resultado_mongo.empty:
        print("Procesando registros fallidos en MongoDB...")

        db = conectar_mongo()
        if db is None:
            print("No se pudo conectar a MongoDB.")
            return
        
        for index, row in resultado_mongo.iterrows():
            id_respaldo = row['id_Respaldo']
            record = {
                "id_Respaldo": id_respaldo,
                "nombre": row['nombre'],
                "numero_identidad": row['numero_identidad'],
                "tipo_identidad": row['tipo_identidad'],
                "direccion": row['direccion'],
                "foto": row['foto'],
                "cargo": row['cargo'],
                "hv": row['hv']
            }   

            if row['error'] == "Insertar - MongoDB":
                print("Insertando registro en MongoDB...")
                insert_data(record, "mongodb")
            elif row['error'] == "Actualizar - MongoDB":
                print("Actualizando registro en MongoDB...")
                update_data(record, "mongodb")
        
        failed_records = failed_records[~failed_records['error'].str.contains("MongoDB", na=False)]
    
def sync_data():
    start_time = datetime.datetime.now()
    while True:
        print(f"Ejecutando tarea de base de datos...{datetime.datetime.now()}, {datetime.datetime.now() - start_time} segundos transcurridos")
        print(f"{failed_records}")

        if not failed_records.empty:
            procesar_registros_mysql()
            procesar_registros_mongo()
        
        time.sleep(10)

