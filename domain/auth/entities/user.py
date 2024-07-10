from typing import Dict, List

from pydantic import BaseModel


class User:
    __id: str
    __email: str
    __password: str
    __roles: List[str]

    def __init__(
        self,
        _id: str = None,
        email: str = None,
        password: str = None,
        roles: List[str] = None,
    ) -> None:
        self.__id = _id
        self.__email = email
        self.__password = password
        self.__roles = roles if roles is not None else ['guest']

    def get(self) -> BaseModel:
        return BaseModel(
            id=self.__id,
            email=self.__email,
            password=self.__password,
            roles=self.__roles,
        )
