from sqlalchemy import create_engine
from sqlalchemy import text
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = getenv('POSTGRES_USER')
passwd = getenv("POSTGRES_PASSWORD")
host = getenv("HOST")
port = getenv("PORT")
database = getenv("POSTGRES_DB")


class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Create instance")
            cls.__instance = super(*args, **kwargs).__new__(cls)

        print("Return instance")
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            print("Connector initialized")
            self.engine = create_engine(f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}", echo=True)
            self.SessionLocal = sessionmaker(autoflush=False, bind=self.engine)
            self._initialized = True

    def select(self, sql):
        res = self.SessionLocal().execute(text(sql))
        return res.all()

    def insert(self, sql):
        trans = self.SessionLocal().begin()
        # key = trans.session.execute(text(sql)).fetchone()
        trans.session.execute(text(sql))
        trans.commit()
        trans.close()
