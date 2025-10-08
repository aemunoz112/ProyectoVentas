import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.database import get_db_connection

class RolController:


    def create_rol(self, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO roles (nombre, descripcion, created_at, updated_at)
                VALUES (%s, %s, NOW(), NOW())
            """
            values = (data.nombre, data.descripcion)
            cursor.execute(query, values)
            conn.commit()
            return {"message": "Rol creado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles")
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron roles")
            payload = []
            for data in result:
                content = {
                    "id": data[0],
                    "nombre": data[1],
                    "descripcion": data[2],
                    "created_at": data[3],
                    "updated_at": data[4]
                }
                payload.append(content)
            return {"roles": jsonable_encoder(payload)}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_rol_by_id(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roles WHERE id = %s", (rol_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            content = {
                "id": result[0],
                "nombre": result[1],
                "descripcion": result[2],
                "created_at": result[3],
                "updated_at": result[4]
            }
            return jsonable_encoder(content)
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def update_rol(self, rol_id: int, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE roles
                SET nombre = %s, descripcion = %s, updated_at = NOW()
                WHERE id = %s
            """
            values = (data.nombre, data.descripcion, rol_id)
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            return {"message": "Rol actualizado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def delete_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roles WHERE id = %s", (rol_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            return {"message": "Rol eliminado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
