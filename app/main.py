from typing import List
from pathlib import Path
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.core.config import settings
from contextlib import asynccontextmanager
from app.helpers.questions import questions
from app.helpers.services import SurveyServices
from app.core.db import initialize_db, get_db_session
from fastapi import FastAPI, Form, UploadFile, File, Depends
from app.database.dummy_data.populate_database import LoadDummyData
from app.helpers.responses import xml_response_handler, error_responses

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    if settings.initialize_database_schema:
        initialize_db()
        if settings.populate_database:
            dummy_data_file_path = (
                BASE_DIR / "database/dummy_data/user_response.json"
            ).as_posix()
            print("populating DB with dummy data")
            data_directory = (BASE_DIR / "database/dummy_data").as_posix()

            loader = LoadDummyData()
            dummy_json: List[dict] = loader.load_json_file(
                file_path=dummy_data_file_path
            )
            loader.populate_db(
                dummy_json_data=dummy_json, data_directory=data_directory
            )
        yield


app = FastAPI(
    title=settings.app_name,
    summary=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get(path="/")
def home_page():
    return {"Status": "Ok"}


@app.get(path="/api/questions")
def get_questions():
    response_body = questions.to_xml()
    return xml_response_handler.xml_response(data=response_body)


@app.get(path="/api/questions/responses")
def get_question_responses(session: Session = Depends(get_db_session)):
    survey_services = SurveyServices(session=session)
    all_responses_xml_response = survey_services.get_all_responses()
    return all_responses_xml_response


@app.put(path="/api/questions/responses")
def get_question_responses(
    session: Session = Depends(get_db_session),
    full_name: str = Form(...),
    email_address: EmailStr = Form(...),
    gender: str = Form(...),
    description: str = Form(...),
    programming_stack: str = Form(...),
    certificates: List[UploadFile] = File(...),
):
    survey_services = SurveyServices(session=session)
    new_user = survey_services.add_user(
        email_address=email_address,
        full_name=full_name,
        description=description,
        gender=gender,
        programming_stack=programming_stack,
    )
    if new_user:
        for new_certificate in certificates:
            file_name = new_certificate.filename
            file_data = new_certificate.file.read()
            survey_services.add_certificate(
                file_name=file_name, file_data=file_data, email_address=email_address
            )
        certificate_names = [
            new_certificate.filename for new_certificate in certificates
        ]
        xml_response = xml_response_handler.user_submission_response(
            email_address=email_address,
            full_name=full_name,
            description=description,
            gender=gender,
            programming_stack=programming_stack,
            certificates=certificate_names,
            date_responded=new_user.date_responded,
        )
        return xml_response
    else:
        return error_responses.email_already_exists()
