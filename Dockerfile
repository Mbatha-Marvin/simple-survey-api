FROM python:3.11.6-alpine3.18

WORKDIR /simple_survey_api

COPY . .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

