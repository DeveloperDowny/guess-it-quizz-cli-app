"""Pydantic models for question and answer files."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Question(BaseModel):
    """A single multiple-choice question."""

    id: int = Field(gt=0)
    question: str = Field(min_length=1)
    options: list[str] = Field(min_length=2)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Normalize and validate a question prompt."""

        question = value.strip()
        if not question:
            raise ValueError("Question text must not be empty.")
        return question

    @field_validator("options")
    @classmethod
    def validate_options(cls, value: list[str]) -> list[str]:
        """Normalize options and enforce uniqueness."""

        normalized = [item.strip() for item in value]
        if any(not item for item in normalized):
            raise ValueError("Question options must not contain empty values.")
        if len(set(normalized)) != len(normalized):
            raise ValueError("Question options must be unique.")
        return normalized


class QuestionSet(BaseModel):
    """Collection of quiz questions."""

    questions: list[Question] = Field(min_length=1)

    @field_validator("questions")
    @classmethod
    def validate_unique_question_ids(cls, value: list[Question]) -> list[Question]:
        """Ensure question identifiers are unique."""

        question_ids = [question.id for question in value]
        if len(set(question_ids)) != len(question_ids):
            raise ValueError("Question IDs must be unique.")
        return value


class AnswerEntry(BaseModel):
    """Answer value for one question."""

    model_config = ConfigDict(populate_by_name=True)

    question_id: int = Field(alias="question-id", serialization_alias="question-id", gt=0)
    answer: str = Field(min_length=1)

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        """Normalize answer text."""

        answer = value.strip()
        if not answer:
            raise ValueError("Answer must not be empty.")
        return answer


class AnswerSheet(BaseModel):
    """Collection of answers from one participant."""

    answers: list[AnswerEntry]

    @field_validator("answers")
    @classmethod
    def validate_unique_answer_ids(cls, value: list[AnswerEntry]) -> list[AnswerEntry]:
        """Ensure an answer sheet has at most one answer per question."""

        question_ids = [entry.question_id for entry in value]
        if len(set(question_ids)) != len(question_ids):
            raise ValueError("Duplicate question-id values are not allowed in answers.")
        return value

    def to_map(self) -> dict[int, str]:
        """Return answer lookup keyed by question ID."""

        return {entry.question_id: entry.answer for entry in self.answers}
