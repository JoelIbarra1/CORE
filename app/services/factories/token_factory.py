
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "clave123"
ALGORITHM = "HS256"
DEFAULT_EXP_MINUTES = 30

class TokenFactory:
    @staticmethod
    def create(sub: str, tipo: str, expires_in_minutes: int = DEFAULT_EXP_MINUTES):
        payload = {
            "sub": sub,
            "type": tipo,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
