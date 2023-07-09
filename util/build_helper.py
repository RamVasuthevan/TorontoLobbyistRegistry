from typing import List, Type, Callable
from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy.ext.declarative import DeclarativeMeta


def create_table(
    session: Session, Raw_Model: Type, Model: Type, get_row: Callable[[Type], dict]
) -> List:
    assert issubclass(
        Raw_Model, DeclarativeMeta
    ), "Raw_Model should be a SQLAlchemy Model"
    assert issubclass(Model, DeclarativeMeta), "Model should be a SQLAlchemy Model"

    data = [get_row(raw) for raw in Raw_Model.query.all()]

    session.execute(insert(Model), data)
    session.commit()
    return session.query(Model).all()
