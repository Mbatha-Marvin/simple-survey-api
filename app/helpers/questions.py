from typing import List
from app.database.models import QuestionsXmlModel, QuestionBaseXmlModel, OptionXmlModel, OptionsXmlModel, FilePropertiesXmlModel

questions_list = []

full_name = QuestionBaseXmlModel(
    title="full_name",
    input_type="short_text",
    required_field="yes",
    text="What is your full name?",
    description="[Surname] [First Name] [Other Names]",
)

questions_list.append(full_name)


email_address = QuestionBaseXmlModel(
    title="email_address",
    input_type="email",
    required_field="yes",
    text="What is your email address?",
    # description
)

questions_list.append(email_address)


# ################# description ####################

description = QuestionBaseXmlModel(
    title="description",
    input_type="long_text",
    required_field="yes",
    text="Tell us a bit more about yourself",
    # description="[Surname] [First Name] [Other Names]",
)

questions_list.append(description)

# ################ Gender start #########################

gender_options_tags: List[dict] = [
    {"display_value": "Male", "value": "MALE"},
    {"display_value": "Female", "value": "FEMALE"},
    {"display_value": "Other", "value": "OTHER"},
]
gender_options = []
for gender_option in gender_options_tags:
    new_option = OptionXmlModel(
        value=gender_option.get("value", ""),
        option_str=gender_option.get("display_value", ""),
    )
    gender_options.append(new_option)

gender_options_instance = OptionsXmlModel(multiple="no", options=gender_options)

gender = QuestionBaseXmlModel(
    title="gender",
    input_type="choice",
    required_field="yes",
    text="What is your gender?",
    options=gender_options_instance,
)

questions_list.append(gender)

# ######################## Programming Stack #########################

programming_stack_options_tags: List[dict] = [
    {"display_value": "React JS", "value": "REACT"},
    {"display_value": "Angular JS", "value": "ANGULAR"},
    {"display_value": "Vue JS", "value": "VUE"},
    {"display_value": "SQL", "value": "SQL"},
    {"display_value": "Postgres", "value": "POSTGRES"},
    {"display_value": "MySQL", "value": "MYSQL"},
    {"display_value": "Microsoft SQL Server", "value": "MSSQL"},
    {"display_value": "Java", "value": "JAVA"},
    {"display_value": "PHP", "value": "PHP"},
    {"display_value": "Go", "value": "GO"},
    {"display_value": "Rust", "value": "RUST"},
]
programming_stack_options = []
for programming_stack_option in programming_stack_options_tags:
    new_option = OptionXmlModel(
        value=programming_stack_option.get("value", ""),
        option_str=programming_stack_option.get("display_value", ""),
    )
    programming_stack_options.append(new_option)

programming_stack_options_instance = OptionsXmlModel(
    multiple="yes", options=programming_stack_options
)

programming_stack = QuestionBaseXmlModel(
    title="programming_stack",
    input_type="choice",
    required_field="yes",
    text="What is your programming_stack?",
    options=programming_stack_options_instance,
)

questions_list.append(programming_stack)

# ################# File Uploads section #################

file_properties = FilePropertiesXmlModel(
    file_format=".pdf",
    max_file_size=1,
    max_file_size_unit="mb",
    multiple="yes"
)
file_upload = QuestionBaseXmlModel(
    title="certificates",
    input_type="file",
    required_field="yes",
    text="You can upload multiple (.pdf)",
    file_properties=file_properties
)

questions_list.append(file_upload)


questions = QuestionsXmlModel(questions=questions_list)
