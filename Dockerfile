FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./api_pulumi /code/api_pulumi

CMD ["uvicorn", "api_pulumi.app:app", "--host", "0.0.0.0", "--port", "8000"]
