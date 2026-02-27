# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 MySQL дерекқор URL (өз логин/парольді қой)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345@localhost/mini_instagram"

# 🔹 Engine жасау
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # SQL сұрауларын console-да көру үшін
    future=True
)

# 🔹 SessionLocal – DB сессиясын алу үшін
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# 🔹 Base – барлық ORM модельдер осыдан мұра алады
Base = declarative_base()

# 🔹 FastAPI Depends үшін DB сессия генераторы
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

