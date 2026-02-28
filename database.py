import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Мәліметтер қорының сілтемесін алу
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Егер айнымалы жоқ болса (локальді режим)
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345@localhost/mini_instagram"

# 2. Render-дегі PostgreSQL сілтемесін түзету
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Engine баптаулары
# PostgreSQL үшін "future=True" қажет емес (SQLAlchemy 2.0-де ол стандарт)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 4. Session және Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. Dependency (FastAPI үшін)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()