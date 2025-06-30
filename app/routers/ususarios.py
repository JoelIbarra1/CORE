from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from models import (
    Pregunta,
    RespuestaUsuario,
    RespuestaUsuarioCreate,
    CompatibilidadDetalle,
    ResultadoCompatibilidad
)
from database import get_db
from auth import get_current_user
from services.compatibilidad import calcular_compatibilidad_preguntas, guardar_resultado_compatibilidad

router = APIRouter(tags=["Usuario"])

# ---------- PREGUNTAS ----------
@router.get("/preguntas", response_model=List[Pregunta])
async def get_preguntas_for_user():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM preguntas ORDER BY categoria, peso DESC")
        preguntas = cursor.fetchall()
        return [Pregunta(**dict(p)) for p in preguntas]

# ---------- RESPUESTAS ----------
@router.post("/respuestas", response_model=dict)
async def create_user_respuesta(respuesta: RespuestaUsuarioCreate):
    if not respuesta.id_usuario:
        respuesta.id_usuario = 1  # Por defecto (temporal)

    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO respuestas_usuario (id_usuario, id_pregunta, respuesta)
                VALUES (?, ?, ?)
            """, (respuesta.id_usuario, respuesta.id_pregunta, respuesta.respuesta))
            conn.commit()
            return {"message": "Respuesta guardada exitosamente"}
        except:
            raise HTTPException(status_code=400, detail="Error al guardar la respuesta")

@router.get("/mis-respuestas/{id_usuario}", response_model=List[RespuestaUsuario])
async def get_my_respuestas(id_usuario: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM respuestas_usuario WHERE id_usuario = ?", (id_usuario,))
        respuestas = cursor.fetchall()
        return [RespuestaUsuario(**dict(r)) for r in respuestas]

# ---------- COMPATIBILIDAD ----------
@router.post("/calcular-compatibilidad/{otro_usuario_id}", response_model=CompatibilidadDetalle)
async def calcular_compatibilidad_con_usuario(otro_usuario_id: int, current_user_data = Depends(get_current_user)):
    user = current_user_data["user"]
    usuario_actual_id = user["id_usuario"]

    if usuario_actual_id == otro_usuario_id:
        raise HTTPException(status_code=400, detail="No puedes calcular compatibilidad contigo mismo")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = ?", (otro_usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

    resultado = calcular_compatibilidad_preguntas(usuario_actual_id, otro_usuario_id)

    if resultado["porcentaje_compatibilidad"] > 0:
        guardar_resultado_compatibilidad(usuario_actual_id, otro_usuario_id, resultado["porcentaje_compatibilidad"])

    return CompatibilidadDetalle(
        id_usuario_origen=usuario_actual_id,
        id_usuario_comparado=otro_usuario_id,
        porcentaje_compatibilidad=resultado["porcentaje_compatibilidad"],
        detalles_calculo=resultado["detalles_calculo"],
        total_ponderado=resultado["total_ponderado"],
        suma_pesos=resultado["suma_pesos"]
    )

@router.get("/mis-compatibilidades", response_model=List[ResultadoCompatibilidad])
async def get_mis_compatibilidades(current_user_data = Depends(get_current_user)):
    user = current_user_data["user"]
    usuario_id = user["id_usuario"]

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM resultados_compatibilidad
            WHERE id_usuario_origen = ?
            ORDER BY porcentaje_compatibilidad DESC
        """, (usuario_id,))
        resultados = cursor.fetchall()
        return [ResultadoCompatibilidad(**dict(r)) for r in resultados]

@router.get("/mejores-matches", response_model=List[dict])
async def get_mejores_matches(
    usuario_id: int = Query(...),
    limite: int = Query(10)
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rc.*, u.nombre, u.ubicacion, u.genero
            FROM resultados_compatibilidad rc
            JOIN usuarios u ON rc.id_usuario_comparado = u.id_usuario
            WHERE rc.id_usuario_origen = ?
            ORDER BY rc.porcentaje_compatibilidad DESC
            LIMIT ?
        """, (usuario_id, limite))
        matches = cursor.fetchall()
        return [
            {
                "usuario_comparado": {
                    "id_usuario": m["id_usuario_comparado"],
                    "nombre": m["nombre"],
                    "ubicacion": m["ubicacion"],
                    "genero": m["genero"]
                },
                "porcentaje_compatibilidad": m["porcentaje_compatibilidad"],
                "fecha_calculo": m["created_at"]
            }
            for m in matches
        ]
