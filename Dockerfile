#install python
FROM python:3.10.4-slim

#grab the code
COPY . /app

#go into the cod's dir
WORKDIR /app

#create a venv
RUN python3 -m venv /opt/venv

# /opt/venv/bin/python
RUN /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r requirements.txt

# run our app
CMD /opt/venv/bin/gunicorn DjangoPMS.wsgi:application --bind "0.0.0.0:8000"