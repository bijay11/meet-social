from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:learndb@localhost:5433/meetsocial"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This below directly uses postgres library, not sqlalchemy to connect to DB. Keeping here for reference.
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', port=5433, database='meetsocial', user='postgres', password='learndb', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connecting to the database failed.")
#         print("Error:", error)
#         time.sleep(2)
