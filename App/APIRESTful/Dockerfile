FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install pymongo[srv] 
RUN pip3 install passlib
RUN pip3 install Flask-HTTPAuth
RUN pip install -U flask-cors

WORKDIR /api
RUN apt update && apt install nano
RUN mkdir img

COPY api.py .
COPY tools.py .
COPY database.py .
COPY config.py .
ENV FLASK_APP=api.py

ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0