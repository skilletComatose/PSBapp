from config import credentials,collection,databaseName,adminDatabase,Admincollection,verysecret,ALLOWED_EXTENSIONS,CORS_HEADERS,UPLOAD_FOLDER                                 
from tools import ReadJson,ManagePsb,OK,BAD,SaveImage,ManageKeys,admin,Admin_ReadJson,chech_token
from flask import send_from_directory,make_response
from flask_cors import CORS, cross_origin
from flask import Flask,request,jsonify
from bson.objectid import ObjectId
import datetime
from msg import * #here are all messages


#we will work with 3 status,
#A(active)
#I(inactive)
#V(validate , it's meaning that admin have to do a verification)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = CORS_HEADERS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = verysecret #very secret is a secret key set it in config.py

folder = app.config['UPLOAD_FOLDER']

@app.route("/")
def hello():
    return hello1

@app.route("/api/psb/", methods=['GET', 'POST'])
@cross_origin()
def psbPost():
    data = request.form.to_dict() #data is a dict with multipart/form-data
    dataKey = "psb"
    imageKey ="img"   
    
    if( request.method == "POST" and data ):
        if dataKey not in data :
            return BAD( "error with json file ", msg4, 400)
        d = data[dataKey] #datakey is the json key where psb informations are (psb is a key in data dict     )
        Json = ReadJson( d ) 
        dictionary = Json.Decode()
        if( Json.Validate( dictionary ) ):
            img = SaveImage( ALLOWED_EXTENSIONS ) 
            media = request.files
            if(imageKey not in media and imageKey in data ):
                return BAD( err1, msg3 , 400)
                
            if(imageKey not in media):
                return BAD (err3, msg2, 400 )      
            
            img.Save( imageKey, folder ) # imagekey is the key with image was posted
            ImageId = img.name
            #ban = not ImageId.strip() #return true if string is empty
            if( ImageId is not None):
                client = ManagePsb(credentials,databaseName)
                query = {
                            "latitude" :dictionary["latitude"] ,
                            "longitude":dictionary["longitude"],                                    
                        }
                Projection = {
                                "status":1,
                                "_id":0
                             }     
                cursor = client.Filter( collection, query=query,Projection=Projection ) 
                c = cursor.count()
                if( c == 0 ):
                    json = Json.Decode()  
                    client.Save( json ,collection, img.name )
                    img.Upload()
                
                else:
                   return BAD (msg5, warning, 409)                
            else:
                return BAD( err1, msg ,400) 
            
            
            return OK(msg1, 201)
        
        else:
            return BAD( msg6 ,Json.missing, 400 )
    
    if(request.method == "GET"):
        client = ManagePsb(credentials,databaseName)   

        key = 'status'
        value = [ 'A', 'a']
        operator = '$in'  
        Projection = {
                      'longitude':1,
                       'latitude':1,
                       'imageId':1,
                        "_id":0
                     } 

        cursor = client.Filter(collection, Key=key, Value=value,  Operator=operator, Projection=Projection)
        info = list(cursor)
        newInfo = ManageKeys(info)
        newInfo.PutId()                               
        return newInfo.LikeJson()
   

@app.route("/api/psb/image/<ImageName>", methods=['GET'])
def ImageResponse(ImageName):
        filename = ImageName
        try:
            return send_from_directory(folder,filename, as_attachment=True)                                 
        except:
            BAD(err3, msg7, 404)

@app.route("/api/psb/statistics",methods=['GET'])
def ReturnData():
    client = ManagePsb(credentials,databaseName)
    projection = {
                    'imageId':0,
                        "_id":0
                 }
    cursor = client.Filter(collection, Projection=projection)
    info = list(cursor)
    newInfo = ManageKeys(info)
    return newInfo.LikeJson()
    

    

@app.route('/api/admin', methods = ['POST'])
@cross_origin()
def new_user():
    if( request.method == "POST"):
        username = request.json.get('username')
        Adminpass = request.json.get('password')
        if username is None or Adminpass is None:
            return BAD(err4, msg8, 400)
    
  
        client = admin(credentials,adminDatabase )
        projection = { 'username':1 }
                        
        cursor = client.Filter(Admincollection, Projection=projection)
        c = cursor.count()
        if(c == 0):
            pwd = client.hash_password( Adminpass, app.config.get('SECRET_KEY'))
            client.Save(Admincollection,username,pwd)
            return OK(msg9, 201)
        else:
            return BAD(err4, msg10, 409)



@app.route('/api/admin', methods = ['GET'])
@cross_origin()
def listpsb():
    ok = chech_token(app.config.get('SECRET_KEY'))
    if False in ok:
        return BAD(err5, ok[1], ok[2])#ok[2] is response code

    client = ManagePsb(credentials,databaseName)
    cursor = client.Filter(collection)
    info = list(cursor)
    newInfo = ManageKeys(info)
    for data in info:
        data['_id'] = str( data['_id'] )

    return newInfo.LikeJson()


@app.route("/api/admin/<psb_id>", methods=['PUT','DELETE'])
def deletePsb(psb_id):
    ok = chech_token(app.config.get('SECRET_KEY'))
    if False in ok:
        return BAD(err5, ok[1], ok[2]) #ok[1] return message obtained from validation and ok[2] return response code

    req = request.get_json()
    if (request.method == 'PUT'):
        data = Admin_ReadJson(req)
        dictionary = data.Decode()
        if(data.Validate(dictionary) and data.Status( dictionary )):
            change = { 'status':dictionary['status'] }
                      
            if(ObjectId.is_valid(psb_id)):
                query = { '_id':ObjectId(psb_id) }
                          
            else:
                return BAD(err4, msg11, 400)

            client = admin( credentials,databaseName )
            ok = client.Update(collection,query,change)
            if(ok):
                return OK(msg12, 200)
            else:
                return BAD(err4, msg13, 406)
        else:
            return BAD(msg6, data.missing , 400 )     

    if (request.method == 'DELETE'):
        if(ObjectId.is_valid(psb_id)):
            
            query = { '_id':ObjectId(psb_id) }
                              
            client = admin(credentials, databaseName )
            ok = client.Delete(collection,query)                     
            if(ok):
                return OK(msg14, 200)
            else:
                return BAD(msg4,msg15, 404)

        else:
            return BAD(msg4, msg16, 400)            


@app.route('/api/login',methods=['POST'])
def login():
    if (request.method == 'POST'):

        username = request.json.get('username')
        Adminpass = request.json.get('password')
        if username is None or Adminpass is None:
            return BAD(err4, msg8, 400)    

        client = admin(credentials,adminDatabase )
        projection = {
                      'password':1,
                       '_id':0 
                     }
        
        query = { 'username':username }
                                  
        cursor = client.Filter(Admincollection, query=query,Projection=projection)
        cursor = list(cursor)
        try:
            hashpw = cursor[0]['password']
        except:
            return BAD(msg3, msg17, 400)
        
        if(client.chech_hash( Adminpass, hashpw, app.config.get('SECRET_KEY') ) ):
            token = client.encode_auth_token(username,app.config.get('SECRET_KEY'))
            response = { 'auth_token': token.decode() }
            return OK(response,200)
        else:
            return BAD(err4, msg17 ,400)

@app.route('/api/logout',methods=['GET'])
def logout():
    ok = chech_token(app.config.get('SECRET_KEY'))
    if False in ok:
        return BAD(err5, ok[1], ok[2])#ok[1] return message, ok[2] return response code  #ok[3] return token already validated
    invalid_token = {
                        'token':ok[3],
                        'time':datetime.datetime.utcnow()
                    }
    client = admin(credentials,adminDatabase )
    client.Black_list(blacklistName, invalid_token)
    return OK(logout1, 200)