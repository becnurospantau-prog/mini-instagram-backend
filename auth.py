from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid
import crud, database, models  # сенің жобаңдағы модульдер

# 🔹 Пароль хэштеу схемасы
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 JWT параметрлері
SECRET_KEY = "supersecretkey"  # Кейін .env файлға ауыстыру керек
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 сағат

# 🔹 OAuth2 схема (Swagger Authorize үшін)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# -------------------------------
# 🔹 Пароль хэштеу және тексеру
# -------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------
# 🔹 JWT токен жасау
# -------------------------------
def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 🔹 Refresh token жасау (UUID)
def create_refresh_token() -> str:
    return str(uuid.uuid4())

# -------------------------------
# 🔹 Ағымдағы user-ды алу (Depends)
# -------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user  # Енді толық User объектісі қайтады
