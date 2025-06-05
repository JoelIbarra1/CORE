from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, date
import sqlite3
from contextlib import contextmanager
from enum import Enum
import json
import re
from fastapi.middleware.cors import CORSMiddleware


# Configuración
SECRET_KEY = "clave123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inicializar FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Configurar hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurar seguridad
security = HTTPBearer()

# Enums
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

class Genero(str, Enum):
    masculino = "masculino"
    femenino = "femenino"
    no_binario = "no_binario"
    prefiero_no_decir = "prefiero_no_decir"

# Modelos Pydantic
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
    user_id: Optional[int] = None  # "user" o "admin"

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

# Base de datos SQLite
DATABASE = "compatibility_app.db"

def init_db():
    """Inicializar la base de datos con todas las tablas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            genero TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla Administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores (
            id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla Preguntas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            peso REAL DEFAULT 1.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla Opciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opciones (
            id_opcion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pregunta INTEGER NOT NULL,
            texto_opcion TEXT NOT NULL,
            FOREIGN KEY (id_pregunta) REFERENCES preguntas (id_pregunta) ON DELETE CASCADE
        )
    ''')
    
    # Tabla RespuestasUsuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas_usuario (
            id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_pregunta INTEGER NOT NULL,
            respuesta TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_pregunta) REFERENCES preguntas (id_pregunta) ON DELETE CASCADE,
            UNIQUE(id_usuario, id_pregunta)
        )
    ''')
    
    # Tabla ResultadosCompatibilidad
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados_compatibilidad (
            id_resultado INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario_origen INTEGER NOT NULL,
            id_usuario_comparado INTEGER NOT NULL,
            porcentaje_compatibilidad REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario_origen) REFERENCES usuarios (id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_usuario_comparado) REFERENCES usuarios (id_usuario) ON DELETE CASCADE,
            UNIQUE(id_usuario_origen, id_usuario_comparado)
        )
    ''')
    
    # Crear administrador por defecto
    admin_password = get_password_hash("admin123")
    cursor.execute('''
        INSERT OR IGNORE INTO administradores (nombre, email, contraseña_hash)
        VALUES (?, ?, ?)
    ''', ("Administrador", "admin@admin.com", admin_password))
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """Context manager para conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Funciones de utilidad
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: str):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario AS id, * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None

def get_admin_by_email(email: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM administradores WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return dict(row)
    return None

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["contraseña_hash"]):
        return False
    return dict(user)  


def authenticate_admin(email: str, password: str):
    admin = get_admin_by_email(email)
    if not admin:
        return False
    if not verify_password(password, admin["contraseña_hash"]):
        return False
    return admin

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("type")
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    if user_type == "admin":
        admin = get_admin_by_email(email)
        if admin is None:
            raise credentials_exception
        return {"user": admin, "type": "admin"}

def calcular_compatibilidad_preguntas(usuario1_id: int, usuario2_id: int):
    """
    Calcula la compatibilidad entre dos usuarios basada en sus respuestas
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Obtener todas las preguntas con sus pesos
        cursor.execute("SELECT * FROM preguntas ORDER BY id_pregunta")
        preguntas = cursor.fetchall()
        
        # Obtener respuestas de ambos usuarios
        cursor.execute("""
            SELECT r1.id_pregunta, r1.respuesta as respuesta1, r2.respuesta as respuesta2, p.peso, p.tipo, p.texto
            FROM respuestas_usuario r1
            JOIN respuestas_usuario r2 ON r1.id_pregunta = r2.id_pregunta
            JOIN preguntas p ON r1.id_pregunta = p.id_pregunta
            WHERE r1.id_usuario = ? AND r2.id_usuario = ?
        """, (usuario1_id, usuario2_id))
        
        respuestas_comunes = cursor.fetchall()
        
        if not respuestas_comunes:
            return {
                "porcentaje_compatibilidad": 0.0,
                "detalles_calculo": [],
                "total_ponderado": 0.0,
                "suma_pesos": 0.0,
                "mensaje": "No hay respuestas comunes entre los usuarios"
            }
        
        total_ponderado = 0.0
        suma_pesos = 0.0
        detalles_calculo = []
        
        for respuesta in respuestas_comunes:
            id_pregunta = respuesta["id_pregunta"]
            respuesta1 = respuesta["respuesta1"]
            respuesta2 = respuesta["respuesta2"]
            peso = respuesta["peso"]
            tipo = respuesta["tipo"]
            texto_pregunta = respuesta["texto"]
            
            coincidencia = calcular_coincidencia_por_tipo(respuesta1, respuesta2, tipo)
            puntos_ponderados = coincidencia * peso
            
            total_ponderado += puntos_ponderados
            suma_pesos += peso
            
            detalles_calculo.append({
                "pregunta_id": id_pregunta,
                "pregunta_texto": texto_pregunta,
                "tipo": tipo,
                "respuesta_usuario1": respuesta1,
                "respuesta_usuario2": respuesta2,
                "coincidencia": round(coincidencia, 3),
                "peso": peso,
                "puntos_ponderados": round(puntos_ponderados, 3)
            })
        
        porcentaje_compatibilidad = (total_ponderado / suma_pesos * 100) if suma_pesos > 0 else 0
        
        return {
            "porcentaje_compatibilidad": round(porcentaje_compatibilidad, 2),
            "detalles_calculo": detalles_calculo,
            "total_ponderado": round(total_ponderado, 3),
            "suma_pesos": suma_pesos
        }

def calcular_coincidencia_por_tipo(respuesta1: str, respuesta2: str, tipo: str) -> float:
    """
    Calcula la coincidencia entre dos respuestas según el tipo de pregunta
    """
    if tipo == "binaria":
        # Respuestas binarias: 1 si son iguales, 0 si son diferentes
        return 1.0 if respuesta1.lower() == respuesta2.lower() else 0.0
    
    elif tipo == "multiple":
        # Respuestas múltiples: usar índice de Jaccard (intersección/unión)
        try:
            # Asume que las respuestas múltiples están separadas por coma
            opciones1 = set([opt.strip().lower() for opt in respuesta1.split(',')])
            opciones2 = set([opt.strip().lower() for opt in respuesta2.split(',')])
            
            interseccion = len(opciones1.intersection(opciones2))
            union = len(opciones1.union(opciones2))
            
            return interseccion / union if union > 0 else 0.0
        except:
            # Si hay error en el parsing, tratar como binaria
            return 1.0 if respuesta1.lower() == respuesta2.lower() else 0.0
    
    elif tipo == "escala":
        # Respuestas de escala: 1 - (diferencia absoluta / rango máximo)
        try:
            val1 = float(respuesta1)
            val2 = float(respuesta2)
            
            # Asume escala de 1 a 5 
            rango_maximo = 4.0  # 5 - 1 = 4
            diferencia = abs(val1 - val2)
            
            return max(0.0, 1.0 - (diferencia / rango_maximo))
        except:
            return 0.0
    
def guardar_resultado_compatibilidad(usuario1_id: int, usuario2_id: int, porcentaje: float):
    """
    Guarda el resultado de compatibilidad en la base de datos
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO resultados_compatibilidad 
                (id_usuario_origen, id_usuario_comparado, porcentaje_compatibilidad)
                VALUES (?, ?, ?)
            """, (usuario1_id, usuario2_id, porcentaje))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
        else:
            user = get_user_by_email(email)
            if user is None:
                raise credentials_exception
            return {"user": user, "type": "user"}

async def get_current_admin(current_user_data = Depends(get_current_user)):
    if current_user_data["type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador"
        )
    return current_user_data["user"]

# Rutas de autenticación
@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/register", response_model=dict)
async def register_user(user: UserRegister):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    hashed_password = get_password_hash(user.contraseña)
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contraseña_hash, fecha_nacimiento, genero, ubicacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user.nombre, user.email, hashed_password, user.fecha_nacimiento, user.genero, user.ubicacion))
            conn.commit()
            user_id = cursor.lastrowid
            return {"message": "Usuario registrado exitosamente", "user_id": user_id}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Error al crear el usuario")

@app.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    user = authenticate_user(user_credentials.email, user_credentials.contraseña)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "type": "user"}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "user",
        "user_id": user["id_usuario"] 
    }

@app.post("/admin/login", response_model=Token)
async def login_admin(admin_credentials: AdminLogin):
    admin = authenticate_admin(admin_credentials.email, admin_credentials.contraseña)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin["email"], "type": "admin"}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user_type": "admin"}

# CRUD de Usuarios (Solo Admin)
@app.post("/admin/usuarios", response_model=dict)
async def create_user_by_admin(user: UsuarioCreate, admin = Depends(get_current_admin)):
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
        user_id = cursor.lastrowid
        return {"message": "Usuario creado exitosamente", "user_id": user_id}

@app.get("/admin/usuarios", response_model=List[Usuario])
async def get_all_users(admin = Depends(get_current_admin), skip: int = 0, limit: int = 100):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios LIMIT ? OFFSET ?", (limit, skip))
        users = cursor.fetchall()
        return [Usuario(**dict(user)) for user in users]

@app.get("/admin/usuarios/{user_id}", response_model=Usuario)
async def get_user_by_id(user_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return Usuario(**dict(user))

@app.put("/admin/usuarios/{user_id}", response_model=dict)
async def update_user(user_id: int, user_update: UsuarioUpdate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verificar que el usuario existe
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Construir query dinámico
        updates = []
        values = []
        for field, value in user_update.dict(exclude_unset=True).items():
            updates.append(f"{field} = ?")
            values.append(value)
        
        if updates:
            values.append(user_id)
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id_usuario = ?"
            cursor.execute(query, values)
            conn.commit()
        
        return {"message": "Usuario actualizado exitosamente"}

@app.delete("/admin/usuarios/{user_id}", response_model=dict)
async def delete_user(user_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        conn.commit()
        return {"message": "Usuario eliminado exitosamente"}

# CRUD de Preguntas (Solo Admin)
@app.post("/admin/preguntas", response_model=dict)
async def create_pregunta(pregunta: PreguntaCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO preguntas (texto, tipo, categoria, peso)
            VALUES (?, ?, ?, ?)
        """, (pregunta.texto, pregunta.tipo, pregunta.categoria, pregunta.peso))
        conn.commit()
        pregunta_id = cursor.lastrowid
        return {"message": "Pregunta creada exitosamente", "pregunta_id": pregunta_id}

@app.get("/admin/preguntas", response_model=List[Pregunta])
async def get_all_preguntas(admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM preguntas")
        preguntas = cursor.fetchall()
        return [Pregunta(**dict(pregunta)) for pregunta in preguntas]

# CRUD de Opciones (Solo Admin)
@app.post("/admin/opciones", response_model=dict)
async def create_opcion(opcion: OpcionCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO opciones (id_pregunta, texto_opcion)
            VALUES (?, ?)
        """, (opcion.id_pregunta, opcion.texto_opcion))
        conn.commit()
        opcion_id = cursor.lastrowid
        return {"message": "Opción creada exitosamente", "opcion_id": opcion_id}

@app.get("/admin/opciones/{pregunta_id}", response_model=List[Opcion])
async def get_opciones_by_pregunta(pregunta_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM opciones WHERE id_pregunta = ?", (pregunta_id,))
        opciones = cursor.fetchall()
        return [Opcion(**dict(opcion)) for opcion in opciones]

# CRUD de Respuestas de Usuario (Solo Admin)
@app.post("/admin/respuestas", response_model=dict)
async def create_respuesta_usuario(respuesta: RespuestaUsuarioCreate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO respuestas_usuario (id_usuario, id_pregunta, respuesta)
                VALUES (?, ?, ?)
            """, (respuesta.id_usuario, respuesta.id_pregunta, respuesta.respuesta))
            conn.commit()
            respuesta_id = cursor.lastrowid
            return {"message": "Respuesta creada exitosamente", "respuesta_id": respuesta_id}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="El usuario ya respondió esta pregunta")

@app.get("/admin/respuestas", response_model=List[RespuestaUsuario])
async def get_all_respuestas(admin = Depends(get_current_admin), user_id: Optional[int] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM respuestas_usuario WHERE id_usuario = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM respuestas_usuario")
        respuestas = cursor.fetchall()
        return [RespuestaUsuario(**dict(respuesta)) for respuesta in respuestas]

@app.put("/admin/respuestas/{respuesta_id}", response_model=dict)
async def update_respuesta_usuario(respuesta_id: int, respuesta_update: RespuestaUsuarioUpdate, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE respuestas_usuario SET respuesta = ? WHERE id_respuesta = ?", 
                      (respuesta_update.respuesta, respuesta_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")
        conn.commit()
        return {"message": "Respuesta actualizada exitosamente"}

@app.delete("/admin/respuestas/{respuesta_id}", response_model=dict)
async def delete_respuesta_usuario(respuesta_id: int, admin = Depends(get_current_admin)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM respuestas_usuario WHERE id_respuesta = ?", (respuesta_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")
        conn.commit()
        return {"message": "Respuesta eliminada exitosamente"}

# Rutas para usuarios regulares
@app.get("/preguntas", response_model=List[Pregunta])
async def get_preguntas_for_user():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM preguntas ORDER BY categoria, peso DESC")
        preguntas = cursor.fetchall()
        return [Pregunta(**dict(pregunta)) for pregunta in preguntas]

@app.post("/respuestas", response_model=dict)
async def create_user_respuesta(respuesta: RespuestaUsuarioCreate):
    # Como no hay autenticación, debes asegurarte de que id_usuario esté en el request
    # O asignar un usuario por defecto
    if not respuesta.id_usuario:
        respuesta.id_usuario = 1  # Usuario por defecto
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO respuestas_usuario (id_usuario, id_pregunta, respuesta)
                VALUES (?, ?, ?)
            """, (respuesta.id_usuario, respuesta.id_pregunta, respuesta.respuesta))
            conn.commit()
            return {"message": "Respuesta guardada exitosamente"}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Error al guardar la respuesta")

@app.get("/mis-respuestas/{id_usuario}", response_model=List[RespuestaUsuario])
async def get_my_respuestas(id_usuario: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM respuestas_usuario WHERE id_usuario = ?", (id_usuario,))
        respuestas = cursor.fetchall()
        return [RespuestaUsuario(**dict(respuesta)) for respuesta in respuestas]

# Endpoints de Compatibilidad
@app.post("/calcular-compatibilidad/{otro_usuario_id}", response_model=CompatibilidadDetalle)
async def calcular_compatibilidad_con_usuario(
    otro_usuario_id: int, 
    current_user_data = Depends(get_current_user)
):
    """Calcula la compatibilidad entre el usuario actual y otro usuario específico"""
    user = current_user_data["user"]
    usuario_actual_id = user["id_usuario"]
    
    if usuario_actual_id == otro_usuario_id:
        raise HTTPException(status_code=400, detail="No puedes calcular compatibilidad contigo mismo")
    
    # Verificar que el otro usuario existe
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = ?", (otro_usuario_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Calcular compatibilidad
    resultado = calcular_compatibilidad_preguntas(usuario_actual_id, otro_usuario_id)
    
    # Guardar resultado en base de datos
    if resultado["porcentaje_compatibilidad"] > 0:
        guardar_resultado_compatibilidad(
            usuario_actual_id, 
            otro_usuario_id, 
            resultado["porcentaje_compatibilidad"]
        )
    
    return CompatibilidadDetalle(
        id_usuario_origen=usuario_actual_id,
        id_usuario_comparado=otro_usuario_id,
        porcentaje_compatibilidad=resultado["porcentaje_compatibilidad"],
        detalles_calculo=resultado["detalles_calculo"],
        total_ponderado=resultado["total_ponderado"],
        suma_pesos=resultado["suma_pesos"]
    )

@app.get("/mis-compatibilidades", response_model=List[ResultadoCompatibilidad])
async def get_mis_compatibilidades(current_user_data = Depends(get_current_user)):
    """Obtiene todas las compatibilidades calculadas para el usuario actual"""
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
        return [ResultadoCompatibilidad(**dict(resultado)) for resultado in resultados]

@app.post("/admin/calcular-compatibilidad-masiva", response_model=dict)
async def calcular_compatibilidades_masivas(admin = Depends(get_current_admin)):
    """Calcula la compatibilidad entre todos los pares de usuarios (solo admin)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM usuarios")
        usuarios = cursor.fetchall()
        usuario_ids = [u["id_usuario"] for u in usuarios]
    
    resultados_procesados = 0
    errores = 0
    
    # Calcular compatibilidad para cada par de usuarios
    for i in range(len(usuario_ids)):
        for j in range(i + 1, len(usuario_ids)):
            usuario1_id = usuario_ids[i]
            usuario2_id = usuario_ids[j]
            
            try:
                # Calcular compatibilidad en ambas direcciones
                resultado1 = calcular_compatibilidad_preguntas(usuario1_id, usuario2_id)
                resultado2 = calcular_compatibilidad_preguntas(usuario2_id, usuario1_id)
                
                # Guardar ambos resultados
                if resultado1["porcentaje_compatibilidad"] > 0:
                    guardar_resultado_compatibilidad(
                        usuario1_id, usuario2_id, resultado1["porcentaje_compatibilidad"]
                    )
                    resultados_procesados += 1
                
                if resultado2["porcentaje_compatibilidad"] > 0:
                    guardar_resultado_compatibilidad(
                        usuario2_id, usuario1_id, resultado2["porcentaje_compatibilidad"]
                    )
                    resultados_procesados += 1
                    
            except Exception as e:
                errores += 1
                continue
    
    return {
        "message": "Cálculo masivo de compatibilidades completado",
        "resultados_procesados": resultados_procesados,
        "errores": errores,
        "total_usuarios": len(usuario_ids)
    }

@app.get("/admin/compatibilidades", response_model=List[ResultadoCompatibilidad])
async def get_all_compatibilidades(
    admin = Depends(get_current_admin),
    usuario_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    limite: int = Query(100, description="Límite de resultados")
):
    """Obtiene todas las compatibilidades del sistema (solo admin)"""
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
        return [ResultadoCompatibilidad(**dict(resultado)) for resultado in resultados]

@app.get("/mejores-matches", response_model=List[dict])
async def get_mejores_matches(
    usuario_id: int = Query(..., description="ID del usuario"),
    limite: int = Query(10, description="Número de mejores matches a retornar")
):
    """Obtiene los mejores matches del usuario sin requerir autenticación"""
    
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
                    "id_usuario": match["id_usuario_comparado"],
                    "nombre": match["nombre"],
                    "ubicacion": match["ubicacion"],
                    "genero": match["genero"]
                },
                "porcentaje_compatibilidad": match["porcentaje_compatibilidad"],
                "fecha_calculo": match["created_at"]
            }
            for match in matches
        ]

@app.get("/")
async def root():
    return {
        "message": "API de Compatibilidad con Sistema de Administración",
        "endpoints": {
            "POST /register": "Registrar usuario",
            "POST /login": "Login usuario",
            "POST /admin/login": "Login administrador",
            "GET /preguntas": "Ver preguntas (usuario)",
            "POST /respuestas": "Crear respuesta (usuario)",
            "GET /mis-respuestas": "Ver mis respuestas (usuario)",
            "POST /calcular-compatibilidad/{user_id}": "Calcular compatibilidad con usuario",
            "GET /mis-compatibilidades": "Ver mis compatibilidades",
            "GET /mejores-matches": "Ver mejores matches",
            "POST /admin/calcular-compatibilidad-masiva": "Calcular todas las compatibilidades (admin)",
            "GET /admin/compatibilidades": "Ver todas las compatibilidades (admin)",
            "Admin CRUD": "Todas las operaciones CRUD para admin"
        },
        "admin_default": {
            "email": "admin@admin.com",
            "password": "admin123"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)