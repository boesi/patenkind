FROM python:slim AS parser
WORKDIR /usr/src/app
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/*.py .
CMD ["python", "./files.py"]

