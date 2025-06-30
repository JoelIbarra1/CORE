from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from services.factories.token_factory import TokenFactory

from models import UserRegister, UserLogin, AdminLogin, Token
from database import get_db
from auth import (
    get_password_hash,
    authenticate_user,
    authenticate_admin,
    create_access_token
)

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register", response_model=dict)
async def register_user(user: UserRegister):
    from auth import get_user_by_email  # evitar import circular

    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(user.contraseña)

    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contraseña_hash, fecha_nacimiento, genero, ubicacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user.nombre,
                user.email,
                hashed_password,
                user.fecha_nacimiento,
                user.genero,
                user.ubicacion
            ))
            conn.commit()
            return {"message": "Usuario registrado exitosamente", "user_id": cursor.lastrowid}
        except:
            raise HTTPException(status_code=400, detail="Error al registrar el usuario")

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    user = authenticate_user(user_credentials.email, user_credentials.contraseña)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Crear el token de acceso
    access_token = TokenFactory.create(
        sub=user["email"],
        tipo="user",
        expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "user",
        "user_id": user["id_usuario"]
    }

@router.post("/admin/login", response_model=Token)
async def login_admin(admin_credentials: AdminLogin):
    admin = authenticate_admin(admin_credentials.email, admin_credentials.contraseña)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": admin["email"], "type": "admin"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "admin",
        "user_id": admin["id_admin"]
    }
