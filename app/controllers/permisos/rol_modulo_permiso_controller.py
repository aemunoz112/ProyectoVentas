import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.database import get_db_connection

class RolModuloPermisoController:

    
    def create_rol_modulo_permiso(self, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO rol_modulo_permisos (rol_id, modulo_id, permiso_id, permitido, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
            """
            values = (data.rol_id, data.modulo_id, data.permiso_id, data.permitido)
            cursor.execute(query, values)
            conn.commit()
            return {"message": "Permiso asignado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_all_rol_modulo_permisos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rmp.id, r.nombre AS rol, m.nombre AS modulo, p.nombre AS permiso, rmp.permitido,
                       rmp.created_at, rmp.updated_at
                FROM rol_modulo_permisos rmp
                JOIN roles r ON rmp.rol_id = r.id
                JOIN modulos m ON rmp.modulo_id = m.id
                JOIN permisos p ON rmp.permiso_id = p.id
            """)
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    "id": data[0],
                    "rol": data[1],
                    "modulo": data[2],
                    "permiso": data[3],
                    "permitido": bool(data[4]),
                    "created_at": data[5],
                    "updated_at": data[6]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron permisos")
            return {"resultados": json_data}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_rol_modulo_permiso_by_id(self, permiso_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM rol_modulo_permisos WHERE id = %s
            """, (permiso_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Permiso no encontrado")
            content = {
                "id": result[0],
                "rol_id": result[1],
                "modulo_id": result[2],
                "permiso_id": result[3],
                "permitido": bool(result[4]),
                "created_at": result[5],
                "updated_at": result[6]
            }
            return jsonable_encoder(content)
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def update_rol_modulo_permiso(self, permiso_id: int, data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE rol_modulo_permisos
                SET rol_id = %s, modulo_id = %s, permiso_id = %s, permitido = %s, updated_at = NOW()
                WHERE id = %s
            """
            values = (data.rol_id, data.modulo_id, data.permiso_id, data.permitido, permiso_id)
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Permiso no encontrado")
            return {"message": "Permiso actualizado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def delete_rol_modulo_permiso(self, permiso_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rol_modulo_permisos WHERE id = %s", (permiso_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Permiso no encontrado")
            return {"message": "Permiso eliminado correctamente"}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    
    def get_permisos_por_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.nombre AS modulo, p.nombre AS permiso, rmp.permitido
                FROM rol_modulo_permisos rmp
                JOIN modulos m ON rmp.modulo_id = m.id
                JOIN permisos p ON rmp.permiso_id = p.id
                WHERE rmp.rol_id = %s
            """, (rol_id,))
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="Este rol no tiene permisos asignados")
            payload = []
            for row in result:
                content = {
                    "modulo": row[0],
                    "permiso": row[1],
                    "permitido": bool(row[2])
                }
                payload.append(content)
            return {"rol_id": rol_id, "permisos": jsonable_encoder(payload)}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
