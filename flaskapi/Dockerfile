FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive


RUN apt update && apt upgrade -y
RUN apt install nginx -y
RUN apt install git nano -y

RUN apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y

RUN apt install python3-venv -y

RUN apt install systemctl -y
RUN mkdir /home/flask

COPY . /home/

RUN ln -s /home/flask-api /var/www/

# RUN cd /var/www/flask-api && source /var/www/flask-api/venv/bin/activate && pip install -r requirements.txt

RUN cp /home/flask-api.service /etc/systemd/system/

COPY flask-api.service /etc/systemd/system/

RUN cp /home/flask /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/flask /etc/nginx/sites-enabled