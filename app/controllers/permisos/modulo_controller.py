import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.database import get_db_connection

class ModuloController:

    
    def create_modulo(self, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO modulos (nombre, descripcion, ruta, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
            """
            values = (data.nombre, data.descripcion, data.ruta)
            cursor.execute(query, values)
            conn.commit()
            return {"message": "Módulo creado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_modulos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulos")
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron módulos")
            payload = []
            for data in result:
                content = {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "ruta": data[3],
                    "created_at": data[4],
                    "updated_at": data[5]
                }
                payload.append(content)
            return {"modulos": jsonable_encoder(payload)}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_modulo_by_id(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM modulos WHERE id = %s", (modulo_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Módulo no encontrado")
            content = {
                "id": result[0],
                "nombre": result[1],
                "descripcion": result[2],
                "ruta": result[3],
                "created_at": result[4],
                "updated_at": result[5]
            }
            return jsonable_encoder(content)
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def update_modulo(self, modulo_id: int, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE modulos
                SET nombre = %s, descripcion = %s, ruta = %s, updated_at = NOW()
                WHERE id = %s
            """
            values = (data.nombre, data.descripcion, data.ruta, modulo_id)
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Módulo no encontrado")
            return {"message": "Módulo actualizado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def delete_modulo(self, modulo_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM modulos WHERE id = %s", (modulo_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Módulo no encontrado")
            return {"message": "Módulo eliminado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
