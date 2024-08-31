from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import (
    CheckConstraint,
    Column,
    DateTime,
    Field,
    ForeignKey,
    Relationship,
    SQLModel,
    Table,
)


class Config:
    arbitrary_types_allowed = True


class AnswersQuestions(SQLModel, table=True):
    __tablename__ = "answers_questions"

    answers_id: UUID = Field(foreign_key="answers.id", primary_key=True)
    questions_answers_id: UUID = Field(
        foreign_key="questions_answers.id", primary_key=True
    )


class UserRole(SQLModel, table=True):
    __tablename__ = "user_role"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permission"

    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permissions.id", primary_key=True)


class AnswersModel(SQLModel, table=True):
    __tablename__ = "answers"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    device_location: Optional[str] = Field(default=None)
    issue_id: UUID = Field(foreign_key="election_issues.id")
    user_id: UUID = Field(foreign_key="users.id")
    interviewed_id: UUID = Field(foreign_key="interviewed.id")

    election_issue: "ElectionIssuesModel" = Relationship(back_populates="answer")
    user: "UsersModel" = Relationship(back_populates="answer")
    interviewed: "InterviewedModel" = Relationship(back_populates="answer")

    questions_answers: List["QuestionsAnswersModel"] = Relationship(
        back_populates="answers",
        link_model=AnswersQuestions,
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class BlacklistTokenModel(SQLModel, table=True):
    __tablename__ = "blacklist_tokens"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    token: str = Field(nullable=False, unique=True)

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class ElectionIssuesModel(SQLModel, table=True):
    __tablename__ = "election_issues"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    type: str = Field(nullable=False, max_length=50)
    title: str = Field(nullable=False, max_length=255)
    location: str = Field(nullable=False, max_length=255)
    year: int = Field(nullable=False)

    questions: List["QuestionsModel"] = Relationship(back_populates="election_issue")

    answer: List[AnswersModel] = Relationship(
        back_populates="election_issue",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "dynamic"},
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class InterviewedModel(SQLModel, table=True):
    __tablename__ = "interviewed"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    profession: str = Field(nullable=False)
    age: int = Field(nullable=False)
    marital_status: str = Field(nullable=False)
    gender: str = Field(nullable=False)
    education_level: str = Field(nullable=False)
    neighborhood: str = Field(nullable=False)
    household_income: str = Field(nullable=False)
    own_house: str = Field(nullable=False)
    religion: str = Field(nullable=False)

    answer: List[AnswersModel] = Relationship(
        back_populates="interviewed",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "dynamic"},
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class OptionsModel(SQLModel, table=True):
    __tablename__ = "options"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    text: str = Field(nullable=False, max_length=255)
    question_id: UUID = Field(foreign_key="questions.id")

    question: "QuestionsModel" = Relationship(back_populates="options")
    answer: List["QuestionsAnswersModel"] = Relationship(back_populates="option_answer")

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class PermissionModel(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=50)

    roles: List["RolesModel"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class QuestionsAnswersModel(SQLModel, table=True):
    __tablename__ = "questions_answers"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    question_id: UUID = Field(foreign_key="questions.id")
    option_id: Optional[UUID] = Field(foreign_key="options.id")
    response: Optional[str] = Field(default=None)

    question: "QuestionsModel" = Relationship(back_populates="answer")
    option_answer: "OptionsModel" = Relationship(back_populates="answer")

    answers: List[AnswersModel] = Relationship(
        back_populates="questions_answers",
        link_model=AnswersQuestions,
    )

    __table_args__ = (
        CheckConstraint(
            "(option_id IS NOT NULL AND response IS NULL) OR (option_id IS NULL AND response IS NOT NULL)",
            name="option_or_response_check",
        ),
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class QuestionsModel(SQLModel, table=True):
    __tablename__ = "questions"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    text: str = Field(nullable=False, max_length=255)
    election_issues_id: UUID = Field(foreign_key="election_issues.id")

    election_issue: "ElectionIssuesModel" = Relationship(back_populates="questions")
    options: List[OptionsModel] = Relationship(back_populates="question")
    answer: List[QuestionsAnswersModel] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "dynamic"},
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )

    class Config(Config):
        pass


class RolesModel(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)

    permissions: List[PermissionModel] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
    )
    users: List["UsersModel"] = Relationship(
        back_populates="roles",
        link_model=UserRole,
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )


class UsersModel(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)

    roles: List[RolesModel] = Relationship(
        back_populates="users",
        link_model=UserRole,
    )

    answer: List[AnswersModel] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "dynamic"},
    )

    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
        description="Data de criação.",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=datetime.now),
        description="Data da última atualização.",
    )
