import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Егер Render-де DATABASE_URL айнымалысы болса, соны алады (PostgreSQL үшін)
# 2. Егер ол жоқ болса (локально), сенің MySQL базаңды қолданады
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Осы жерге өзіңнің MySQL сілтемеңді қалдыр (локалды тексеру үшін)
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345@localhost/mini_instagram"

# Render-дегі PostgreSQL сілтемесін SQLAlchemy түсінетіндей форматқа келтіру
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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

