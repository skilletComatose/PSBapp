FROM python:3.6-buster 
RUN pip3 install Flask
RUN pip3 install pymongo[srv] 
RUN pip3 install -U flask-cors
RUN pip3 install flask-restx
RUN pip3 install pyjwt==1.4.2
RUN pip3 install bcrypt  
RUN pip3 install Werkzeug==0.16.0  


WORKDIR /api

ENV FLASK_APP=api.py

ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0