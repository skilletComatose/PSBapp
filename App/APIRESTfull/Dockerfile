FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install pymongo
RUN apt update && apt install nano
COPY api.py .
COPY tools.py .
COPY database.py .

ENV FLASK_APP=api.py

ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0