from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from models import (
    Usuario, UsuarioCreate, UsuarioUpdate,
    Pregunta, PreguntaCreate,
    Opcion, OpcionCreate,
    RespuestaUsuario, RespuestaUsuarioCreate, RespuestaUsuarioUpdate,
    ResultadoCompatibilidad
)

from auth import get_current_admin
from database import get_db
from services.compatibilidad import (
    calcular_compatibilidad_preguntas,
    guardar_resultado_compatibilidad
)

router = APIRouter(prefix="/admin", tags=["Admin"])

# ---------- USUARIOS ----------
@router.post("/usuarios", response_model=dict)
async def create_user(user: UsuarioCreate, admin = Depends(get_current_admin)):
    from auth import get_user_by_email, get_password_hash
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(user.contraseña)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, contraseña_hash, fecha_nacimiento, genero, ubicacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user.nombre, user.email, hashed_password, user.fecha_nacimiento, user.genero, user.ubicacion))
        conn.commit()
        return {"message": "Usuario creado exitosamente", "user_id": cursor.lastrowid}

@router.get("/usuarios", response_model=List[Usuario])
async def get_all_users(admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return [Usuario(**dict(u)) for u in usuarios]

@router.get("/usuarios/{user_id}", response_model=Usuario)
async def get_user_by_id(user_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return Usuario(**dict(user))

@router.put("/usuarios/{user_id}", response_model=dict)
async def update_user(user_id: int, update: UsuarioUpdate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        campos = []
        valores = []

        for campo, valor in update.dict(exclude_unset=True).items():
            campos.append(f"{campo} = ?")
            valores.append(valor)

        if not campos:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        valores.append(user_id)
        cursor.execute(f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = ?", valores)
        conn.commit()
        return {"message": "Usuario actualizado"}

@router.delete("/usuarios/{user_id}", response_model=dict)
async def delete_user(user_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        conn.commit()
        return {"message": "Usuario eliminado"}

# ---------- PREGUNTAS ----------
@router.post("/preguntas", response_model=dict)
async def create_pregunta(pregunta: PreguntaCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO preguntas (texto, tipo, categoria, peso)
            VALUES (?, ?, ?, ?)
        """, (pregunta.texto, pregunta.tipo, pregunta.categoria, pregunta.peso))
        conn.commit()
        return {"message": "Pregunta creada", "pregunta_id": cursor.lastrowid}

@router.get("/preguntas", response_model=List[Pregunta])
async def get_all_preguntas(admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM preguntas")
        preguntas = cursor.fetchall()
        return [Pregunta(**dict(p)) for p in preguntas]

# ---------- OPCIONES ----------
@router.post("/opciones", response_model=dict)
async def create_opcion(opcion: OpcionCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO opciones (id_pregunta, texto_opcion)
            VALUES (?, ?)
        """, (opcion.id_pregunta, opcion.texto_opcion))
        conn.commit()
        return {"message": "Opción creada", "opcion_id": cursor.lastrowid}

@router.get("/opciones/{pregunta_id}", response_model=List[Opcion])
async def get_opciones_by_pregunta(pregunta_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM opciones WHERE id_pregunta = ?", (pregunta_id,))
        opciones = cursor.fetchall()
        return [Opcion(**dict(o)) for o in opciones]

# ---------- RESPUESTAS ----------
@router.post("/respuestas", response_model=dict)
async def create_respuesta(respuesta: RespuestaUsuarioCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO respuestas_usuario (id_usuario, id_pregunta, respuesta)
                VALUES (?, ?, ?)
            """, (respuesta.id_usuario, respuesta.id_pregunta, respuesta.respuesta))
            conn.commit()
            return {"message": "Respuesta creada", "respuesta_id": cursor.lastrowid}
        except:
            raise HTTPException(status_code=400, detail="Error al guardar la respuesta")

@router.get("/respuestas", response_model=List[RespuestaUsuario])
async def get_all_respuestas(admin = Depends(get_current_admin), user_id: Optional[int] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM respuestas_usuario WHERE id_usuario = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM respuestas_usuario")
        respuestas = cursor.fetchall()
        return [RespuestaUsuario(**dict(r)) for r in respuestas]

@router.put("/respuestas/{respuesta_id}", response_model=dict)
async def update_respuesta(respuesta_id: int, data: RespuestaUsuarioUpdate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE respuestas_usuario SET respuesta = ? WHERE id_respuesta = ?", (data.respuesta, respuesta_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")
        conn.commit()
        return {"message": "Respuesta actualizada"}

@router.delete("/respuestas/{respuesta_id}", response_model=dict)
async def delete_respuesta(respuesta_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM respuestas_usuario WHERE id_respuesta = ?", (respuesta_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")
        conn.commit()
        return {"message": "Respuesta eliminada"}

# ---------- COMPATIBILIDADES ----------
@router.post("/calcular-compatibilidad-masiva", response_model=dict)
async def calcular_compatibilidades(admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios")
        ids = [row["id_usuario"] for row in cursor.fetchall()]

    procesados = 0
    errores = 0

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            u1, u2 = ids[i], ids[j]
            try:
                r1 = calcular_compatibilidad_preguntas(u1, u2)
                r2 = calcular_compatibilidad_preguntas(u2, u1)

                if r1["porcentaje_compatibilidad"] > 0:
                    guardar_resultado_compatibilidad(u1, u2, r1["porcentaje_compatibilidad"])
                    procesados += 1

                if r2["porcentaje_compatibilidad"] > 0:
                    guardar_resultado_compatibilidad(u2, u1, r2["porcentaje_compatibilidad"])
                    procesados += 1

            except:
                errores += 1
                continue

    return {
        "message": "Compatibilidades calculadas",
        "resultados_procesados": procesados,
        "errores": errores,
        "total_usuarios": len(ids)
    }

@router.get("/compatibilidades", response_model=List[ResultadoCompatibilidad])
async def get_all_compatibilidades(
    admin = Depends(get_current_admin),
    usuario_id: Optional[int] = Query(None),
    limite: int = Query(100)
):
    with get_db() as conn:
        cursor = conn.cursor()
        if usuario_id:
            cursor.execute("""
                SELECT * FROM resultados_compatibilidad
                WHERE id_usuario_origen = ? OR id_usuario_comparado = ?
                ORDER BY porcentaje_compatibilidad DESC
                LIMIT ?
            """, (usuario_id, usuario_id, limite))
        else:
            cursor.execute("""
                SELECT * FROM resultados_compatibilidad
                ORDER BY porcentaje_compatibilidad DESC
                LIMIT ?
            """, (limite,))
        resultados = cursor.fetchall()
        return [ResultadoCompatibilidad(**dict(r)) for r in resultados]
