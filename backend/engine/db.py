import os
from typing import Dict, List
import sqlalchemy as db
from dotenv import load_dotenv

# current_dir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(current_dir, '.env'))

print("DB credentials")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print(DB_USER)
print(DB_PASS)
print(DB_ADDRESS)
print(DB_PORT)
print(DB_NAME)

class Session:
    engine = None
    conn = None

    def __init__(self):
        try:
            self.engine = db.create_engine(
                f"postgresql://{DB_USER}:{DB_PASS}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
            )
            print("Engine created")
        except:
            print("Can't create 'engine")
            raise

    def start(self):
        try:
            self.conn = self.engine.connect()
            print("Connection started")
        except:
            print("Can't start connection")
            raise

    def stop(self):
        self.conn.close()
        print("Connection stopped")

    def create_table(self, table_name: str):
        metadata = db.MetaData()

        db.Table(
            table_name,
            metadata,
            db.Column("ID", db.Integer, primary_key=True),
            db.Column("IMG_URL", db.VARCHAR),
            db.Column("Convolution", db.LargeBinary),
            db.Column("PAGE_URL", db.VARCHAR),
            db.Column("PAGE_TITLE", db.VARCHAR),
            db.Column("WEBSITE", db.VARCHAR),
        )

        metadata.create_all(self.engine)

    def get_table(self, table_name: str):
        metadata = db.MetaData()
        metadata.reflect(bind=self.engine)

        return metadata.tables[table_name]

    def insert(self, table_name: str, values_list: List[Dict[str, List[float]]]):
        table = self.get_table(table_name)
        query = db.insert(table)
        self.conn.execute(query, values_list)
        self.conn.commit()
