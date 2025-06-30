# repositories/usuario_repo.py

from database import get_db

class UsuarioRepository:

    @staticmethod
    def get_by_email(email: str):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_id(user_id: int):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def list_all():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(usuario_dict: dict):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contraseña_hash, fecha_nacimiento, genero, ubicacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                usuario_dict["nombre"],
                usuario_dict["email"],
                usuario_dict["contraseña_hash"],
                usuario_dict["fecha_nacimiento"],
                usuario_dict["genero"],
                usuario_dict["ubicacion"]
            ))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def delete(user_id: int):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
