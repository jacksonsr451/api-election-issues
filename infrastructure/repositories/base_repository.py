from abc import ABC

from pydantic import BaseModel as BaseDataModel
from sqlalchemy.orm import Session

from infrastructure.adapters.database import Session as SessionLocal
from infrastructure.exceptions.database_exception import DatabaseException
from infrastructure.models import BaseModelSQL


class BaseRepository(ABC):
    def __init__(self, model: BaseModelSQL):
        self.__model = model
        self.db: Session = SessionLocal()

    def create(self, data: BaseDataModel) -> BaseModelSQL | None:
        try:
            data = data.model_dump()
            create_data = self.__model.from_model(**data)
            self.db.add(create_data)
            return self._extracted_from_update_5(create_data)
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with id {id} not found', status_code=404
            )

    def update(self, id: str, data: BaseDataModel) -> BaseModelSQL | None:
        try:
            instance = (
                self.db.query(self.__model)
                .filter(self.__model.id == id)
                .first()
            )

            if instance:
                for key, value in data.model_dump().items():
                    setattr(instance, key, value)

                return self._extracted_from_update_5(instance)
            return None
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with id {id} not found', status_code=404
            )

    def _extracted_from_update_5(self, arg0):
        self.db.commit()
        self.db.refresh(arg0)
        return arg0

    def delete(self, id: str) -> None:
        try:
            delete_data = (
                self.db.query(self.__model)
                .filter(self.__model.id == id)
                .first()
            )
            self.db.delete(delete_data)
            self.db.commit()
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with id {id} not found', status_code=404
            )

    def delete_by_id_with_key_and_value(self, key: str, value: str) -> None:
        try:
            delete_data = (
                self.db.query(self.__model).filter(getattr(self.__model, key) == value).first()
            )
            self.db.delete(delete_data)
            self.db.commit()
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with {key} {value} not found', status_code=404
            )

    def get_all(self) -> list:
        try:
            return self.db.query(self.__model).all()
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} not found', status_code=404
            )

    def get_by_id(self, id: str) -> BaseModelSQL | None:
        try:
            return (
                self.db.query(self.__model)
                .filter(self.__model.id == id)
                .first()
            )
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with id {id} not found', status_code=404
            )

    def get_all_with_key_and_value(self, key: str, value: str) -> list:
        try:
            return (
                self.db.query(self.__model)
                .filter(getattr(self.__model, key) == value)
                .all()
            )
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with {key} {value} not found', status_code=404
            )

    def get_by_id_with_key_and_value(
        self, key: str, value: str
    ) -> BaseModelSQL | None:
        try:
            return (
                self.db.query(self.__model)
                .filter(self.__model.id == id)
                .filter(getattr(self.__model, key) == value)
                .first()
            )
        except Exception:
            name = self.__model.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with {key} {value} not found', status_code=404
            )
