from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

class Genero(str, Enum):
    masculino = "masculino"
    femenino = "femenino"
    no_binario = "no_binario"
    prefiero_no_decir = "prefiero_no_decir"

class TipoPregunta(str, Enum):
    binaria = "binaria"
    multiple = "multiple"
    escala = "escala"
    texto = "texto"

class CategoriaPregunta(str, Enum):
    valores = "valores"
    intereses = "intereses"
    estilo_vida = "estilo_vida"
    personalidad = "personalidad"

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str
    fecha_nacimiento: date
    genero: Genero
    ubicacion: str

class UserLogin(BaseModel):
    email: str
    contraseña: str

class AdminLogin(BaseModel):
    email: str
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str
    user_id: Optional[int] = None

class Usuario(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    fecha_nacimiento: date
    genero: str
    ubicacion: str

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str
    fecha_nacimiento: date
    genero: Genero
    ubicacion: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Genero] = None
    ubicacion: Optional[str] = None

class PreguntaCreate(BaseModel):
    texto: str
    tipo: TipoPregunta
    categoria: CategoriaPregunta
    peso: float = 1.0

class Pregunta(BaseModel):
    id_pregunta: int
    texto: str
    tipo: str
    categoria: str
    peso: float

class OpcionCreate(BaseModel):
    id_pregunta: int
    texto_opcion: str

class Opcion(BaseModel):
    id_opcion: int
    id_pregunta: int
    texto_opcion: str

class RespuestaUsuarioCreate(BaseModel):
    id_usuario: int
    id_pregunta: int
    respuesta: str

class RespuestaUsuario(BaseModel):
    id_respuesta: int
    id_usuario: int
    id_pregunta: int
    respuesta: str

class RespuestaUsuarioUpdate(BaseModel):
    respuesta: str

class ResultadoCompatibilidad(BaseModel):
    id_resultado: int
    id_usuario_origen: int
    id_usuario_comparado: int
    porcentaje_compatibilidad: float

class CompatibilidadDetalle(BaseModel):
    id_usuario_origen: int
    id_usuario_comparado: int
    porcentaje_compatibilidad: float
    detalles_calculo: List[dict]
    total_ponderado: float
    suma_pesos: float

class Administrador(BaseModel):
    id_admin: int
    nombre: str
    email: str
