import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.database import get_db_connection

class AtributoController:

    # ✅ Crear un nuevo atributo
    def create_atributo(self, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO atributos (nombre, tipo_dato, descripcion, es_requerido, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
            """
            values = (data.nombre, data.tipo_dato, data.descripcion, data.es_requerido)
            cursor.execute(query, values)
            conn.commit()
            return {"message": "Atributo creado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    # ✅ Obtener todos los atributos
    def get_atributos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributos")
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron atributos")
            payload = []
            for data in result:
                content = {
                    "id": data[0],
                    "nombre": data[1],
                    "tipo_dato": data[2],
                    "descripcion": data[3],
                    "es_requerido": bool(data[4]),
                    "created_at": data[5],
                    "updated_at": data[6]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            return {"atributos": json_data}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    # ✅ Obtener atributo por ID
    def get_atributo_by_id(self, atributo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM atributos WHERE id = %s", (atributo_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Atributo no encontrado")
            content = {
                "id": result[0],
                "nombre": result[1],
                "tipo_dato": result[2],
                "descripcion": result[3],
                "es_requerido": bool(result[4]),
                "created_at": result[5],
                "updated_at": result[6]
            }
            return jsonable_encoder(content)
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    # ✅ Actualizar un atributo
    def update_atributo(self, atributo_id: int, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE atributos
                SET nombre = %s, tipo_dato = %s, descripcion = %s,
                    es_requerido = %s, updated_at = NOW()
                WHERE id = %s
            """
            values = (data.nombre, data.tipo_dato, data.descripcion, data.es_requerido, atributo_id)
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Atributo no encontrado")
            return {"message": "Atributo actualizado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    # ✅ Eliminar un atributo
    def delete_atributo(self, atributo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM atributos WHERE id = %s", (atributo_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Atributo no encontrado")
            return {"message": "Atributo eliminado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
