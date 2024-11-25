from conect import conectar_mysql, conectar_mongo  
import pandas as pd

def fetch_data():
    # Conectar a MySQL
    try:
        mysql_db = conectar_mysql()
        query = "SELECT * FROM empleados"
        df_mysql = pd.read_sql(query, mysql_db)
        mysql_db.close()
    except Exception as e:
        print(f"Error al obtener datos de MySQL: {e}")
        df_mysql = pd.DataFrame()  # Base de datos MySQL no disponible

    # Conectar a MongoDB
    try:
        mongo_db = conectar_mongo()
        mongo_collection = mongo_db['empleados']
        df_mongo = pd.DataFrame(list(mongo_collection.find({})))
        mongo_db.close()
    except Exception as e:
        print(f"Error al obtener datos de MongoDB: {e}")
        df_mongo = pd.DataFrame()  # Base de datos MongoDB no disponible

    # Concatenar datos, asegurando eliminar duplicados si ambas bases están disponibles
    df_final = pd.concat([df_mysql, df_mongo]).drop_duplicates().reset_index(drop=True)
    return df_final

def insert_data(record):
    responses = []
    
    # Intentar insertar en MySQL
    try:
        mysql_db = conectar_mysql()
        cursor = mysql_db.cursor()
        query = """
            INSERT INTO empleados (nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
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

    # Intentar insertar en MongoDB
    try:
        mongo_db = conectar_mongo()
        mongo_collection = mongo_db['empleados']
        mongo_collection.insert_one(record)
        responses.append("Registro guardado en MongoDB")
    except Exception as e:
        responses.append(f"Error en MongoDB: {e}")
    finally:
        mongo_db.close()

    return responses

def update_data(record):
    responses = []
    
    # Actualizar en MySQL
    try:
        mysql_db = conectar_mysql()
        cursor = mysql_db.cursor()
        query = """
            UPDATE empleados
            SET nombre = %s, tipo_identidad = %s, direccion = %s, foto = %s, cargo = %s, hv = %s
            WHERE numero_identidad = %s
        """
        values = (
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
        mongo_db = conectar_mongo()
        mongo_collection = mongo_db['empleados']
        mongo_collection.update_one(
            {"numero_identidad": record["numero_identidad"]},
            {"$set": record}
        )
        responses.append("Registro actualizado en MongoDB")
    except Exception as e:
        responses.append(f"Error en MongoDB: {e}")
    finally:
        mongo_db.close()

    return responses
