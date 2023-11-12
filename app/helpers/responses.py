import datetime
import xmltodict, json
from typing import List
from fastapi import Response

from app.database.schemas import UserSchema, CertificateSchema
from app.helpers.get_certificates_by_id import get_certificates
from app.database.models import (
    UserQuestionResponseXmlModel,
    CertificateXmlModel,
    CertificatesXmlModel,
    QuestionResponseXmlModel,
    QuestionResponsesXmlModel,
)


class XmlResponseHandler:
    def xml_response(self, data: bytes) -> Response:
        return Response(content=data, media_type="application/xml")

    def create_all_question_responses_response(
        self, user_responses: List[UserSchema], start_id_number: int = 1
    ) -> Response:
        total_responses = len(user_responses)
        page_size = 10
        last_page = int(total_responses / page_size) + 1

        question_responses_xml_instances_list = []
        for index, user_response in enumerate(user_responses):
            if index < page_size:
                print(index)
                user_id = user_response.id
                user_certificates = get_certificates(user_id=user_id)
                certificates_in_db: List[CertificateSchema] = user_certificates

                print(f"Length of {len(certificates_in_db) = }")
                certificates_list = []

                for certificate_in_db in certificates_in_db:
                    certificate_xml_instance = CertificateXmlModel(
                        certificate=certificate_in_db.file_name
                    )
                    certificates_list.append(certificate_xml_instance)

                certificates_xml_instance = CertificatesXmlModel(
                    certificates=certificates_list
                )
                print(f"Length of {len(certificates_list) = }")

                # date_responded = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                question_response_xml_instance = QuestionResponseXmlModel(
                    full_name=user_response.full_name,
                    email_address=user_response.email_address,
                    description=user_response.description,
                    gender=user_response.gender,
                    programming_stack=user_response.programming_stack,
                    certificates=certificates_xml_instance,
                    date_responded=user_response.date_responded,
                )
                question_responses_xml_instances_list.append(
                    question_response_xml_instance
                )

        question_responses_xml_instance = QuestionResponsesXmlModel(
            current_page=1,
            last_page=last_page,
            page_size=page_size,
            total_count=total_responses,
            question_responses=question_responses_xml_instances_list,
        )

        xml_data = question_responses_xml_instance.to_xml()
        # print(xml_data)
        return self.xml_response(data=xml_data)

    def user_submission_response(
        self,
        email_address: str,
        full_name: str,
        description: str,
        gender: str,
        programming_stack: str,
        certificates: List[str],
        date_responded: str,
    ):
        certificates_list = []
        for certificate in certificates:
            certificate_instance = CertificateXmlModel(certificate=certificate)
            certificates_list.append(certificate_instance)

        certificates_instance = CertificatesXmlModel(certificates=certificates_list)

        user_question_response_instance = UserQuestionResponseXmlModel(
            full_name=full_name,
            email_address=email_address,
            description=description,
            gender=gender,
            programming_stack=programming_stack,
            certificates=certificates_instance,
            date_responded=date_responded,
        ).to_xml()

        return self.xml_response(data=user_question_response_instance)


class ErrorResponses:
    def user_not_found(self):
        return Response(content="User Not Found!!", status_code=404)

    def email_not_found(self):
        return Response(content="Email Not Found!!", status_code=404)
    
    def email_already_exists(self):
        return Response(content="Email Already Exists!!", status_code=404)

    def responses_not_found(self):
        return Response(content="Responses Not Found!!", status_code=404)

    def empty_body_provided(self):
        return Response(content="Empty Request Body Provided!!", status_code=404)

    def request_body_not_xml(self):
        return Response(content="Request Body Not Valid XML !!", status_code=404)


error_responses = ErrorResponses()
xml_response_handler = XmlResponseHandler()
