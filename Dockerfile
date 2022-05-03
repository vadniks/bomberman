FROM python:3.7.13-slim-buster
ADD . /app/
WORKDIR /app/
RUN apt update && apt install -y xauth -qqy x11-apps
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD cd src && python3 main.py
