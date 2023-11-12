from typing import List
from fastapi import Response
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.helpers.responses import error_responses, xml_response_handler
from app.database.schemas import UserSchema, CertificateSchema


class SurveyServices:
    def __init__(self, session: Session) -> None:
        self.session = session

    def email_exists(self, email_address: EmailStr):
        if self.session.scalars(
            select(UserSchema).where(UserSchema.email_address == email_address)
        ).one_or_none():
            return True
        else:
            return False

    def get_user_id(self, email_address: EmailStr):
        if self.email_exists:
            user_details = self.session.scalars(
                select(UserSchema).where(UserSchema.email_address == email_address)
            ).first()
            return user_details.id
        else:
            error_responses.email_not_found()

    def get_user_responses(
        self, email_address: EmailStr
    ) -> List[UserSchema] | Response:
        if self.email_exists(email_address=email_address):
            user_responses = self.session.scalars(
                select(UserSchema).where(UserSchema.email_address == email_address)
            ).all()
            return user_responses
        else:
            error_responses.email_not_found()

    def get_all_responses(self) -> Response:
        all_responses = self.session.scalars(select(UserSchema)).all()
        if all_responses:
            xml_response = xml_response_handler.create_all_question_responses_response(
                user_responses=all_responses
            )
            return xml_response
        else:
            return error_responses.responses_not_found()

    def get_user_certificate_by_id(self, user_id: int) -> List[CertificateSchema]:
        user_details = self.session.scalars(
            select(UserSchema).where(UserSchema.id == user_id)
        ).first()

        return user_details.certificates

    def add_user(
        self,
        email_address: EmailStr,
        full_name: str,
        description: str,
        gender: str,
        programming_stack: str,
    ) -> UserSchema | Response:
        if self.email_exists(email_address=email_address):
            return None
        else:
            new_user = UserSchema(
                email_address=email_address,
                full_name=full_name,
                description=description,
                gender=gender,
                programming_stack=programming_stack,
            )
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user

    def add_certificate(
        self, file_name: str, file_data: bytes, email_address: str
    ) -> CertificateSchema:
        user_id = self.get_user_id(email_address=email_address)
        new_certificate = CertificateSchema(
            file_name=file_name, file_data=file_data, user_id=user_id
        )
        self.session.add(new_certificate)
        self.session.commit()
        self.session.refresh(new_certificate)

        return new_certificate
