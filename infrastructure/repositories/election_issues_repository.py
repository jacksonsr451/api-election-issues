from fastapi import Depends

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
        data = data.model_dump()
        data_questions = data.get('questions', [])
        del data['questions']
        model_instance = ElectionIssuesModel.from_model(**data)
        questions = []
        for question in data_questions:
            options = []
            data_options = question.get('options', [])
            del question['options']
            question_model = QuestionsModel(question)
            for option in data_options:
                option_model = OptionsModel(option)
                self.db.add(option_model)
                options.append(option_model)
            question_model.options = options
            self.db.add(question_model)
            questions.append(question_model)
        model_instance.questions = questions
        self.db.add(model_instance)
        return self._extracted_from_update_5(model_instance)

    def update(self, id: str, data: ElectionIssuesEntity):
        instance = self.db.query(ElectionIssuesModel).filter_by(id=id).first()
        if instance:
            data_dict = data.model_dump()
            data_questions = data_dict.get('questions', [])

            for key, value in data_dict.items():
                setattr(instance, key, value)

            updated_questions = []
            for question_data in data_questions:
                question_id = question_data.get('id')
                options_data = question_data.get('options', [])

                if question_id:
                    question_instance = (
                        self.db.query(QuestionsModel)
                        .filter_by(id=question_id)
                        .first()
                    )
                    if question_instance:
                        for key, value in question_data.items():
                            setattr(question_instance, key, value)
                else:
                    question_instance = QuestionsModel(**question_data)
                    self.db.add(question_instance)

                updated_options = []
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
                                setattr(option_instance, key, value)
                    else:
                        option_instance = OptionsModel(**option_data)
                        self.db.add(option_instance)

                    updated_options.append(option_instance)

                question_instance.options = updated_options
                updated_questions.append(question_instance)

            instance.questions = updated_questions
            self.db.add(instance)
            self.db.commit()

            return instance

        return None
