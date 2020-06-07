from config import credentials, collection, databaseName, adminDatabase, Admincollection, verysecret, ALLOWED_EXTENSIONS, CORS_HEADERS, UPLOAD_FOLDER
from tools import ReadJson, ManagePsb, OK, BAD, SaveImage, ManageKeys, admin, Admin_ReadJson, check_token
from flask import send_from_directory, make_response
from flask_cors import CORS, cross_origin
from flask import Flask, request
from flask_restx import Api,Resource, fields,reqparse
from bson.objectid import ObjectId
from swagger import description,title,service
from swagger_models import psb_post_parameters,admin_post,admin_get
import datetime
from msg import *  # here are all messages


app  = Flask(__name__)
cors = CORS(app)
api  = Api(
            app         = app,
            title       = title,
            description = description
          )

app.config['CORS_HEADERS'] = CORS_HEADERS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = verysecret

folder = app.config['UPLOAD_FOLDER']

demo = api.namespace(service ,description = description)
name = 'test'
model = {
           'id':fields.Integer(description = 'any test') 
        }
model1 = api.model(name,model)

#@app.route("/api/psb/", methods=['GET', 'POST'])
@demo.route('/psb/')
class psb(Resource):
    @cross_origin(Resource)
    @demo.doc('save_psb')
    @api.response(400, E400 )
    @api.response(409,warning)
    @api.expect(psb_post_parameters)
    def post(self):
        """save psb in data base"""
        data = request.form.to_dict()  # data is a dict with multipart/form-data
        if(not data):
            return BAD(err4,msg19,400 )
        dataKey = "psb" # datakey is the json key where psb information's are (psb is a key in data dict     )
        imageKey = "img" # imagekey is the key with image was posted

        if dataKey not in data:
            return BAD(err4, msg4, 400)
        
        d = data[dataKey]
        Json = ReadJson(d)
        dictionary = Json.Decode()
        if(Json.Validate(dictionary)):
            img = SaveImage(ALLOWED_EXTENSIONS)
            media = request.files
            if(imageKey not in media and imageKey in data):
                return BAD(err1, msg3, 400)

            if(imageKey not in media):
                return BAD(err3, msg2, 400)

            
            img.Save(imageKey, folder)
            ImageId = img.name
            
            if(ImageId is not None):
                client = ManagePsb(credentials, databaseName)
                query = {
                        "latitude": dictionary["latitude"],
                        "longitude": dictionary["longitude"],
                        }
                Projection = {
                                "status": 1,
                                "_id"   : 0
                             }
                cursor = client.Filter(
                    collection, query=query, Projection=Projection)
                c = cursor.count()
                if(c == 0):
                    json = Json.Decode()
                    client.Save(json, collection, img.name)
                    img.Upload()

                else:
                    return BAD(msg5, warning, 409)
            else:
                return BAD(err1, msg, 400)

            return OK(msg1, 201)

        else:
            return BAD(msg6, Json.missing, 400)

    def get(self):
        """list actives psb """
        client = ManagePsb(credentials, databaseName)
        key = 'status'
        value = ['A', 'a']
        operator = '$in'
        Projection = {
                        'longitude': 1,
                        'latitude' : 1,
                        'imageId'  : 1,
                        "_id"      : 0
                     }

        cursor = client.Filter(
            collection, Key=key, Value=value,  Operator=operator, Projection=Projection)
        info = list(cursor)
        newInfo = ManageKeys(info)
        newInfo.PutId()
        return newInfo.LikeJson()


#@app.route("/api/psb/image/<ImageName>", methods=['GET'])
@demo.route('/psb/image/<string:ImageName>')
class ImageResponse(Resource):
    @api.response(200,'')
    @api.response(404,msg7)
    def get(self,ImageName):
        """get psb image"""
        filename = ImageName
        try:
            return send_from_directory(folder, filename, as_attachment=True)
        except:
            BAD(err3, msg7, 404)


#@app.route("/api/psb/statistics", methods=['GET'])
@demo.route('/psb/statistics')
class statistics(Resource):    
    def get(self):
        """To get psb data to do statistics"""
        client = ManagePsb(credentials, databaseName)
        projection = {
            'imageId': 0,
            "_id": 0
        }
        cursor = client.Filter(collection, Projection=projection)
        info = list(cursor)
        newInfo = ManageKeys(info)
        return newInfo.LikeJson()


#@app.route('/api/admin', methods=['POST'])
#@demo.route('/admin')
#class new_user(Resource):

    
#@app.route('/api/admin', methods=['GET'])
@demo.route('/admin')
class ListPsb(Resource):
    @cross_origin(Resource)
    @api.expect(admin_get)
    @api.response(400,missing_token)
    @api.response(403,E403)
    def get(self):
        """get exclusive psb data"""
        ok = check_token(app.config.get('SECRET_KEY'))
        if False in ok:
            return BAD(err5, ok[1], ok[2])  # ok[2] is response code

        client = ManagePsb(credentials, databaseName)
        cursor = client.Filter(collection)
        info = list(cursor)
        newInfo = ManageKeys(info)
        for data in info:
            data['_id'] = str(data['_id'])

        return newInfo.LikeJson()

    @cross_origin(Resource)
    @api.response(201,msg9)
    @api.response(400,E400v2)
    @api.response(409,msg10)
    @api.expect(admin_post)
    def post(self):
        """create admin user"""
        try:
            username = request.json.get('username')
            Adminpass = request.json.get('password')
        except:
            return BAD(err4, msg18,400)
        
        if username is None or Adminpass is None:
            return BAD(err4, msg8, 400)

        client = admin(credentials, adminDatabase)
        projection = {'username': 1}

        cursor = client.Filter(Admincollection, Projection=projection)
        c = cursor.count()
        if(c == 0):
            pwd = client.hash_password(Adminpass, app.config.get('SECRET_KEY'))
            client.Save(Admincollection, username, pwd)
            return OK(msg9, 201)
        else:
            return BAD(err4, msg10, 409)



#@app.route("/api/admin/<psb_id>", methods=['PUT', 'DELETE'])
@demo.route('/admin/<string:psb_id>')
class UpdateStatus(Resource):
    @cross_origin(Resource)
    @api.response(200,msg12)
    @api.response(400,E400v3)
    @api.response(403,E403)
    @api.response(406,msg13)
    @api.expect(admin_get)
    def put(self,psb_id):
        """Update psb status"""
        ok = check_token(app.config.get('SECRET_KEY'))
        if False in ok:
            return BAD(err5, ok[1], ok[2])# ok[1] return message obtained from validation and ok[2] return response code
        try: 
            req = request.get_json()
        except:
            return BAD(err4,msg18,400)
        
        data = Admin_ReadJson(req)
        dictionary = data.Decode()
        if(data.Validate(dictionary) and data.Status(dictionary)):
            change = {'status': dictionary['status']}

            if(ObjectId.is_valid(psb_id)):
                query = {'_id': ObjectId(psb_id)}

            else:
                return BAD(err4, msg11, 400)

            client = admin(credentials, databaseName)
            ok = client.Update(collection, query, change)
            if(ok):
                return OK(msg12, 200)
            else:
                return BAD(err4, msg13, 406)
        else:
            return BAD(msg6, data.missing, 400)
    
    @cross_origin(Resource)
    @api.expect(admin_get)
    @api.response(200,msg14)
    @api.response(400,msg16)
    @api.response(403,E403)
    @api.response(404,msg15)
    def delete(self,psb_id):
        """delete psb """
        ok = check_token(app.config.get('SECRET_KEY'))
        if False in ok:
            return BAD(err5, ok[1], ok[2])
        
        if(ObjectId.is_valid(psb_id)):

            query = {'_id': ObjectId(psb_id)}

            client = admin(credentials, databaseName)
            ok = client.Delete(collection, query)
            if(ok):
                return OK(msg14, 200)
            else:
                return BAD(msg11, msg15, 404)

        else:
            return BAD(msg4, msg16, 400)

#@app.route('/api/login', methods=['POST'])
@demo.route('/login')
class login(Resource):
    @cross_origin(Resource)
    @api.response(200,auth_token)
    @api.response(400,E400v4)
    @api.expect(admin_post)
    def post(self):
        """Admin login"""
        try:
            username = request.json.get('username')
            Adminpass = request.json.get('password')
        except:
            return BAD(err4, msg18,400)  
        
        if username is None or Adminpass is None:
            return BAD(err4, msg8, 400)

        client = admin(credentials, adminDatabase)
        projection = {
                        'password': 1,
                        '_id'     : 0
                     }

        query = {'username': username}

        cursor = client.Filter(
            Admincollection, query=query, Projection=projection)
        cursor = list(cursor)
        try:
            hashpw = cursor[0]['password']
        except:
            return BAD(msg3, msg17, 400)

        if(client.check_hash(Adminpass, hashpw, app.config.get('SECRET_KEY'))):
            token = client.encode_auth_token( username, app.config.get('SECRET_KEY') )                
            response = { auth_token_response: token.decode()}
            return OK(response, 200)
        else:
            return BAD(err4, msg17, 400)


#@app.route('/api/logout', methods=['GET'])
@demo.route('/logout')
class logout(Resource):
    @cross_origin(Resource)
    @api.expect(admin_get)
    @api.response(403,E403)
    @api.response(200,log_out)
    def get(self):
        """Admin logout"""
        ok = check_token(app.config.get('SECRET_KEY'))
        if False in ok:
            return BAD(err5, ok[1], ok[2]) # ok[1] return message, ok[2] return response code  #ok[3] return token already validated
        invalid_token = {
                            'token': ok[3],
                            'time': datetime.datetime.utcnow()
                        }
        client = admin(credentials, adminDatabase)
        client.Black_list(blacklistName, invalid_token)
        return OK(logout1, 200)
