from typing import List, Optional
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlalchemy as db

# INTERNAL IMPORTS
from engine.db import Session as S

Base = declarative_base()


# CREATE THE TABLE MODEL TO USE IT FOR QUERYING
class BaseTable(Base):
    __abstract__ = True
    id = db.Column("ID", db.Integer, primary_key=True)
    img_url = db.Column("IMG_URL", db.VARCHAR)
    convolution = db.Column("Convolution", db.LargeBinary)
    page_url = db.Column("PAGE_URL", db.VARCHAR)
    page_title = db.Column("PAGE_TITLE", db.VARCHAR)


class Backup(BaseTable):
    __tablename__ = "publico_backup"


class Updated(BaseTable):
    __tablename__ = "publico_updated"

class Master(BaseTable):
    __tablename__ = "master_db"

TABLES = {
    "publico_backup": Backup,
    "publico_updated": Updated,
    "master_db": Master
}


def get_urls_from_ids(ids: List[int], table: str) -> List[str]:
    """Get the urls from the ids

    Parameters
    ----------
    db_table : db.Table
        The table to query
    ids : List[int]
        The ids of the images

    Returns
    -------
    List[str]
        The urls of the images
    """

    db_table: db.Table = TABLES.get(table)

    Session = sessionmaker(bind=S().engine)
    session = Session()
    print("Querying the database...")
    result = session.query(db_table).filter(db_table.id.in_(ids))
    rows = {row.id: (row.img_url, row.page_url, row.page_title) for row in result}
    print("Done", len(rows))
    return [rows[i] for i in ids]


def get_convolution_from_ids(ids: List[int], table: str) -> List[str]:
    """Get the convolution from the ids

    Parameters
    ----------
    table : str
        The table to query
    ids : List[int]
        The ids of the images

    Returns
    -------
    List[str]
        The urls of the images
    """
    db_table: db.Table = TABLES.get(table)

    Session = sessionmaker(bind=S().engine)
    session = Session()
    result = session.query(db_table).filter(db_table.id.in_(ids))
    convolution = [row.convolution.decode().split(",") for row in result]
    return [[float(i) for i in row] for row in convolution]


def get_all_convolution(table: str, limit: Optional[int] = None) -> List[str]:
    """Get all the images from the database sorted by ascending id

    Returns
    -------
    table : str
        The table to query
    List[str]
        The urls of the images
    """
    db_table: db.Table = TABLES.get(table)

    Session = sessionmaker(bind=S().engine)
    session = Session()
    if limit:
        ids = list(range(limit))
        result = session.query(db_table).order_by(db.asc(db_table.id)).filter(db_table.id.in_(ids))
    else:
        result = session.query(db_table).order_by(db.asc(db_table.id)).all()
    convolution = [row.convolution.decode().split(",") for row in result]
    data = [[float(i) for i in row] for row in convolution]
    return data
