import uuid
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel as BaseDataModel
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.dynamic import AppenderQuery

from infrastructure.adapters.database import Base

T = TypeVar('T', bound='BaseModelSQL')


@as_declarative()
class BaseModelSQL(Base):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now,
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    # Initialize a model with the given kwargs
    #
    # Arguments:
    #     kwargs: A dictionary of key-value pairs to initialize
    #             the model with
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attributes = ', '.join(
            f'{key}={value}'
            for key, value in self.__dict__.items()
            if key != '_sa_instance_state'
        )
        return f'<{class_name}({attributes})>'

    def to_dict(self, visited=None):
        if visited is None:
            visited = set()

        result = {}
        visited.add(self)

        for attr in self.__mapper__.column_attrs:
            value = getattr(self, attr.key)
            if isinstance(value, uuid.UUID):
                result[attr.key] = str(value)
            elif isinstance(value, datetime):
                result[attr.key] = value.isoformat()
            else:
                result[attr.key] = value

        for attr in self.__mapper__.relationships:
            value = getattr(self, attr.key)
            if isinstance(value, (AppenderQuery, InstrumentedList)):
                result[attr.key] = [
                    item.to_dict(visited)
                    for item in value
                    if item not in visited
                ]
            elif value is not None and value not in visited:
                result[attr.key] = value.to_dict(visited)
        return result

    def to_schema(self, schema) -> BaseDataModel:
        model_dict = self.to_dict(visited=set())
        for key, value in model_dict.items():
            if isinstance(value, uuid.UUID):
                model_dict[key] = str(value)
            elif isinstance(value, datetime):
                model_dict[key] = value.isoformat()

        return schema(**model_dict)

    @classmethod
    def _convert_to_schema_value(cls, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            return value

    @classmethod
    def from_model(cls, **kwargs) -> T:
        return cls(**kwargs)

    def __eq__(self, other):
        if isinstance(other, BaseModelSQL):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):
        return hash(self.id)
