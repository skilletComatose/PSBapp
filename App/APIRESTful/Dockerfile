FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install pymongo[srv] 
RUN pip3 install Flask-HTTPAuth
RUN pip3 install -U flask-cors
RUN pip3 install pyjwt==1.4.2
RUN pip3 install bcrypt    


WORKDIR /api

ENV FLASK_APP=api.py

ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0