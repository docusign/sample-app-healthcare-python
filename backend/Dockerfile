FROM python:3.12-slim

ENV DS_TARGET_ACCOUNT_ID='FALSE'

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend/
COPY private.key /backend/


EXPOSE 5001
CMD ["python", "manage.py", "runserver", "0.0.0.0:5001"]