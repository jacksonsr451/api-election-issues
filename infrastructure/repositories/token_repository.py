from infrastructure.models import BlacklistTokenModel
from infrastructure.repositories.base_repository import BaseRepository


class TokenRepository(BaseRepository):
    def __init__(self, model: BlacklistTokenModel):
        super().__init__(model)

    def invite_token(self, token: str):
        model = BlacklistTokenModel.from_model(**{'token': token})
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

    def check_token(self, token: str) -> bool:
        token_in_blacklist = (
            self.db.query(BlacklistTokenModel)
            .filter_by(token=token)
            .first()
        )

        return not bool(token_in_blacklist)
