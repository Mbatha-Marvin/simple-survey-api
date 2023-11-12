from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr


# ################# Question Models ##############################
class OptionXmlModel(BaseXmlModel):
    value: str = attr(name="value")
    option_str: str


class OptionsXmlModel(BaseXmlModel, tag="options"):
    multiple: str = attr(name="multiple")
    options: List[OptionXmlModel] = element(tag="option")


class FilePropertiesXmlModel(BaseXmlModel, tag="file_properties"):
    file_format: str = attr(name="format")
    max_file_size: int = attr(name="max_file_size")
    max_file_size_unit: str = attr(name="max_file_size_unit")
    multiple: str = attr(name="multiple")


class QuestionBaseXmlModel(BaseXmlModel):
    # attributes
    title: str = attr(name="name")
    input_type: str = attr(name="type")
    required_field: str = attr(name="required")

    # element tags
    text: str = element(tag="text")
    description: Optional[str] = element(tag="description", default=None)
    options: Optional[OptionsXmlModel] = None
    file_properties: FilePropertiesXmlModel = None


class QuestionsXmlModel(BaseXmlModel, tag="questions"):
    questions: List[QuestionBaseXmlModel] = element(tag="question")


# ################## QUESTION RESPONSE MODELS #############################

# <question_response>
#   <full_name>Jane Doe</full_name>
#   <email_address>janedoe@gmail.com</email_address>
#   <description>I am an experienced FrontEnd Engineer with over 6 years experience.</description>
#   <gender>MALE</gender>
#   <programming_stack>REACT,VUE</programming_stack>
#   <certificates>
#       <certificate>Adobe Certification 19-08-2023.pdf</certificate>
#       <certificate>Figma Fundamentals 19-08-2023.pdf</certificate>
#   </certificates>
#   <date_responded>2023-09-23 12:30:12</date_responded>
# </question_response>


class CertificateXmlModel(BaseXmlModel):
    certificate: str


class CertificatesXmlModel(BaseXmlModel, tag="certificates"):
    certificates: List[CertificateXmlModel] = element(tag="certificate")


class UserQuestionResponseXmlModel(BaseXmlModel, tag="question_response"):
    full_name: str = element(tag="full_name")
    email_address: str = element(tag="email_address")
    description: str = element(tag="description")
    gender: str = element(tag="gender")
    programming_stack: str = element(tag="programming_stack")
    certificates: CertificatesXmlModel
    date_responded: datetime = element(tag="date_responded")


class QuestionResponseXmlModel(BaseXmlModel, tag="question_response"):
    full_name: str = element(tag="full_name")
    email_address: str = element(tag="email_address")
    description: str = element(tag="description")
    gender: str = element(tag="gender")
    programming_stack: str = element(tag="programming_stack")
    certificates: CertificatesXmlModel
    date_responded: datetime = element(tag="date_responded")


class QuestionResponsesXmlModel(BaseXmlModel, tag="question_responses"):
    current_page: int = attr(name="current_page")
    last_page: int = attr(name="last_page")
    page_size: int = attr(name="page_size")
    total_count: int = attr(name="total_count")
    question_responses: List[QuestionResponseXmlModel]


# class AllResponses(BaseXmlModel)
