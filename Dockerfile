FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /users
COPY requirements.txt /users/
RUN pip install -r requirements.txt
COPY . ./users