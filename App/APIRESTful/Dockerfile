FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install pymongo[srv] 
RUN pip3 install passlib
RUN pip3 install Flask-HTTPAuth
RUN pip3 install -U flask-cors


WORKDIR /api

ENV FLASK_APP=api.py

ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0