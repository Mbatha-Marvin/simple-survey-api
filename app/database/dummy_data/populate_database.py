import json
from typing import List
from pathlib import Path
from app.core.db import engine
from sqlalchemy.orm import Session
from app.helpers.services import SurveyServices


class LoadDummyData:
    def load_json_file(self, file_path: str):
        with open(file=file_path) as json_file:
            file_contents = json_file.read()
            parsed_data = json.loads(file_contents)

        return parsed_data

    def populate_db(self, dummy_json_data: List[dict], data_directory: str):
        with Session(engine) as session:
            survey_services = SurveyServices(session=session)
            for dummy_response in dummy_json_data:
                new_email = dummy_response.get("question_response").get("email_address")

                if survey_services.email_exists(email_address=new_email):
                    print(f"Email Address {new_email} already exists")
                else:
                    email_address = (
                        dummy_response.get("question_response").get("email_address"),
                    )
                    full_name = (
                        dummy_response.get("question_response").get("full_name"),
                    )
                    description = (
                        dummy_response.get("question_response").get("description"),
                    )
                    gender = (dummy_response.get("question_response").get("gender"),)
                    programming_stack = dummy_response.get("question_response").get(
                        "programming_stack"
                    )
                    new_user = survey_services.add_user(
                        email_address=email_address,
                        full_name=full_name,
                        description=description,
                        gender=gender,
                        programming_stack=programming_stack,
                    )
                    # print(new_user)   

                    certificate_title_list: List[str] = (
                        dummy_response.get("question_response")
                        .get("certificates")
                        .get("certificate")
                    )
                    for certificate_title in certificate_title_list:
                        file_name = certificate_title
                        file_path = f"{data_directory}/{certificate_title}"
                        file_data = Path(file_path).read_bytes()

                        new_certificate = survey_services.add_certificate(
                            file_name=file_name,
                            file_data=file_data,
                            email_address=email_address,
                        )
                        print(new_certificate)
