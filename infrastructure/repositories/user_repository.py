from infrastructure.models import UsersModel
from infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: UsersModel):
        BaseRepository.__init__(self, model=model)
