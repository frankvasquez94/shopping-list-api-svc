from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_SOURCE_URL = "sqlite:///./shopping_list.db"

# connect_args= {"check_same_thread": False}
# solo es necesario pa sqlite.
engine = create_engine(
    DATA_SOURCE_URL,
    connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Connection pool
# Para cada peticion  de la funcion
# obtiene una conexion del pool.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
