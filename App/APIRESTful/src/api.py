from flask import Flask,request,jsonify
from tools import ReadJson,ManagePsb,OK,BAD,SaveImage,ManageKeys,admin,Admin_ReadJson,get_header
from flask import send_from_directory,make_response
#from flask_httpauth import HTTPTokenAuth
from bson.objectid import ObjectId
from config import credentials,collection,databaseName,adminDatabase,Admincollection,verysecret                                 
from msg import * #here ara all error message

#auth =  HTTPTokenAuth(scheme='Bearer',realm=auth_failed().message() )
from flask_cors import CORS, cross_origin


#we will work with 3 status,
#A(active)
#I(inactive)
#V(validate , it's meaning that admin have to do a verification)

UPLOAD_FOLDER = '/api/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = verysecret #very secret is a secret key set it in config.py

folder = app.config['UPLOAD_FOLDER']




@app.route("/")
def hello():
    return "<H1>Running ;v<H1/>"

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
                   return BAD ("Warning",warning,409)                
            else:
                return BAD( err1, msg ,400) 
            
            
            return OK(msg1,201)
        
        else:
            return BAD( "error" ,Json.missing, 400 )
    
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
        return send_from_directory(folder,filename, as_attachment=True)                                 


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
def new_user():
    if( request.method == "POST"):
        username = request.json.get('username')
        Adminpass = request.json.get('password')
        if username is None or Adminpass is None:
            return BAD('error','bad request',400)
    
  
        client = admin(credentials,adminDatabase )
        projection = {
                        'username':1
                     }
        cursor = client.Filter(Admincollection, Projection=projection)
        c = cursor.count()
        if(c == 0):
            pwd = client.hash_password( Adminpass, app.config.get('SECRET_KEY'))
            client.Save(Admincollection,username,pwd)
            return OK('user saved',201)
        else:
            return BAD('error','only can exists one admin',409)



@app.route('/api/admin', methods = ['GET'])
def listpsb():
    ok = get_header(app.config.get('SECRET_KEY'))
    if False in ok:
        return BAD('auth failed',ok[1],ok[2])#ok[2] is response code

    client = ManagePsb(credentials,databaseName)
    cursor = client.Filter(collection)
    info = list(cursor)
    newInfo = ManageKeys(info)
    for data in info:
        data['_id'] = str( data['_id'] )

    return newInfo.LikeJson()


@app.route("/api/admin/<psb_id>", methods=['PUT','DELETE'])
def deletePsb(psb_id):
    ok = get_header(app.config.get('SECRET_KEY'))
    if False in ok:
        return BAD('auth failed',ok[1],ok[2])#ok[2] is response code

    req = request.get_json()
    if (request.method == 'PUT'):
        data = Admin_ReadJson(req)
        dictionary = data.Decode()
        if(data.Validate(dictionary) and data.Status( dictionary )):
            change = {
                      'status':dictionary['status']
                     }
            if(ObjectId.is_valid(psb_id)):
                query = {
                          '_id':ObjectId(psb_id)
                        }      
            else:
                return BAD('error','incorect id',400)

            client = admin( credentials,databaseName )
            ok = client.Update(collection,query,change)
            if(ok):
                return OK('updated',200)
            else:
                return BAD('error','not updated',406)
        else:
            return BAD( "error",data.missing , 400 )     

    if (request.method == 'DELETE'):
        if(ObjectId.is_valid(psb_id)):
            query = {
                      '_id':ObjectId(psb_id)
                    }
            client = admin(credentials, databaseName )
            ok = client.Delete(collection,query)                     
            if(ok):
                return OK('removed',200)
            else:
                return BAD('error','not deleted, id not found',404)

        else:
            return BAD('error','incorect id',400)            


@app.route('/api/login',methods=['GET','POST'])
def login():
    if (request.method == 'POST'):

        username = request.json.get('username')
        Adminpass = request.json.get('password')
        if username is None or Adminpass is None:
            return BAD('error','bad request',400)    

        client = admin(credentials,adminDatabase )
        projection = {
                      'password':1,
                       '_id':0 
                     }
        
        query = {
                  'username':username
                }
        cursor = client.Filter(Admincollection, query=query,Projection=projection)
        cursor = list(cursor)
        try:
            hashpw = cursor[0]['password']
        except:
            return BAD('error','cursor do not work',400)
        
        if(client.chech_hash( Adminpass, hashpw,app.config.get('SECRET_KEY'))):
            token = client.encode_auth_token(username,app.config.get('SECRET_KEY'))
            response = {
                        'auth_token': token.decode()
                       }
            return OK(response,200)
        else:
            return BAD('error','Username or Password are incorrect ' ,400)
