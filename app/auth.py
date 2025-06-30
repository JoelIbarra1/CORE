from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from repositories.usuario_repo import UsuarioRepository

from database import get_db
from models import Token
import sqlite3

# Configuración
SECRET_KEY = "clave123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Funciones de autenticación

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_admin_by_email(email: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM administradores WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["contraseña_hash"]):
        return None
    return user

def authenticate_admin(email: str, password: str):
    admin = get_admin_by_email(email)
    if not admin or not verify_password(password, admin["contraseña_hash"]):
        return None
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
        email = payload.get("sub")
        user_type = payload.get("type")
        if email is None or user_type not in ["user", "admin"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if user_type == "admin":
        admin = get_admin_by_email(email)
        if admin is None:
            raise credentials_exception
        return {"user": admin, "type": "admin"}
    else:
        user = get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return {"user": user, "type": "user"}

async def get_current_admin(current_user_data=Depends(get_current_user)):
    if current_user_data["type"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requieren permisos de administrador")
    return current_user_data["user"]

def get_user_by_email(email: str):
    return UsuarioRepository.get_by_email(email)