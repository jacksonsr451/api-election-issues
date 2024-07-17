from sqlalchemy import Column, Text

from infrastructure.models.base_model_sql import BaseModelSQL


class BlacklistTokenModel(BaseModelSQL):
    __tablename__ = 'blacklist_tokens'

    token = Column(Text, nullable=False, unique=True)
