import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1️⃣ Render болса — DATABASE_URL алады
# 2️⃣ Локально болса — MySQL қолданады
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345@localhost/mini_instagram"

# Render PostgreSQL fix
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

# 🔹 Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

# 🔹 Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# 🔹 Base
Base = declarative_base()

# 🔹 FastAPI үшін
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()