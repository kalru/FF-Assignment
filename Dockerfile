# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN python3 -m venv /venv
# install dependencies
COPY requirements.txt /code/
RUN . /venv/bin/activate && pip install -r requirements.txt

COPY main/ /code/

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "main/main.wsgi:application"]