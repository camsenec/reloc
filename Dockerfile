FROM ubuntu:20.04
ENV PYTHONBUFFERED=1

RUN apt -y update &&     \
    apt -y install wget  \
            sudo         \
            git          \
            python3      \
            pip

WORKDIR /app
COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]