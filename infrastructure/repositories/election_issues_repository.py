from fastapi import Depends
from sqlalchemy.orm import joinedload

from domain.election_issues.election_issue_entity import ElectionIssuesEntity
from infrastructure.models import (
    ElectionIssuesModel,
    OptionsModel,
    QuestionsModel,
)
from infrastructure.repositories.base_repository import BaseRepository


class ElectionIssuesRepository(BaseRepository):
    def __init__(
        self, model: ElectionIssuesModel = Depends(ElectionIssuesModel)
    ):
        super().__init__(model=model)

    def create(self, data: ElectionIssuesEntity):
        try:
            data = data.model_dump()

            data_questions = data.get('questions', [])
            del data['questions']

            model_instance = ElectionIssuesModel(
                type=data['type'],
                title=data['title'],
                location=data['location'],
                year=data['year'],
            )

            for question_data in data_questions:
                question = QuestionsModel(
                    text=question_data['text'],
                    created_at=question_data.get('created_at'),
                    updated_at=question_data.get('updated_at'),
                )
                for option_data in question_data.get('options', []):
                    option = OptionsModel(text=option_data['text'])
                    question.options.append(option)

                model_instance.questions.append(question)

            self.db.add(model_instance)
            return self._extracted_from_update_5(model_instance)

        except Exception as e:
            print(f'Erro ao criar registro: {str(e)}')
            self.db.rollback()
            raise

    def update(self, id: str, data: ElectionIssuesEntity):
        try:
            data_dict = data.model_dump()
            instance = (
                self.db.query(ElectionIssuesModel).filter_by(id=id).first()
            )

            if not instance:
                raise ValueError('Instance not found')

            data_questions = data_dict.get('questions', [])
            del data_dict['questions']

            for key, value in data_dict.items():
                if hasattr(instance, key):
                    if (
                        key != 'id'
                        and key in ElectionIssuesModel.__table__.columns.keys()
                    ):
                        setattr(instance, key, value)
            for question_data in data_questions:
                question_id = question_data.get('id')

                options_data = question_data.get('options', [])
                del question_data['options']

                if question_id:
                    question_instance = (
                        self.db.query(QuestionsModel)
                        .filter_by(id=question_id)
                        .first()
                    )
                    if question_instance:
                        for key, value in question_data.items():
                            if hasattr(question_instance, key):
                                if (
                                    key != 'id'
                                    and key
                                    in QuestionsModel.__table__.columns.keys()
                                ):
                                    setattr(question_instance, key, value)
                    else:
                        question_instance = QuestionsModel(**question_data)
                        self.db.add(question_instance)
                else:
                    question_instance = QuestionsModel(**question_data)
                    self.db.add(question_instance)

                for option_data in options_data:
                    option_id = option_data.get('id')
                    if option_id:
                        option_instance = (
                            self.db.query(OptionsModel)
                            .filter_by(id=option_id)
                            .first()
                        )
                        if option_instance:
                            for key, value in option_data.items():
                                if hasattr(option_instance, key):
                                    if (
                                        key != 'id'
                                        and key
                                        in OptionsModel.__table__.columns.keys()
                                    ):
                                        setattr(option_instance, key, value)
                        else:
                            option_instance = OptionsModel(**option_data)
                            self.db.add(option_instance)
                    else:
                        option_instance = OptionsModel(**option_data)
                    question_instance.options.append(option_instance)
                    print(question_instance.id, option_instance.id)
                instance.questions.append(question_instance)
            return self._extracted_from_update_5(instance)

        except Exception as e:
            print(f'Erro ao atualizar registro: {str(e)}')
            self.db.rollback()
            raise e
