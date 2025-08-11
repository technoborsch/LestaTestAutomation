# syntax=docker/dockerfile:1
FROM python:3.13-alpine
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/
WORKDIR /code

CMD ["pytest", "Test_RowingBoat.py", "-v", "--tb=short"]