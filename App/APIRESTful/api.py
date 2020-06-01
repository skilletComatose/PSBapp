from flask import Flask,request,jsonify
from tools import ReadJson,ManagePsb,OK,BAD,SaveImage,ManageKeys,admin,Admin_ReadJson
from flask import send_from_directory,make_response
from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId
from config import * # here are databases names, collections names, and credentials to do connection with Mongo Atlas
auth = HTTPBasicAuth()
#from App.APIRESTful.tools import ReadJson,ManagePsb,OK,BAD,SaveImage,ManageKeys,admin,Admin_ReadJson
#we will work with 3 status,
#A(active)
#I(inactive)
#V(validate , it's meaning that admin have to do a verification)


UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

folder = app.config['UPLOAD_FOLDER']



msg1 = "psb saved successfully!'"
err1 = "Error with image : "
err3 = "Image error >>> Possible errors"
msg = " Error with image : missing image  "
msg2 =  ["1. Field error :key posted not in dict"  , 
         "2. Image field was send empty o.O"       , 
         "3. neither image and key  weren't sent"]
msg3 = "key are ok but, the image wasn't sent :("
msg4 = "Key posted not in dict :("
warning = "The psb sent is already registered, but thanks for send it"


@app.route("/api/psb/", methods=['GET', 'POST'])
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
            ban = not ImageId.strip() #return true if string is empty
            if( ImageId != None and not ban  ):
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
        
        url = 'http://localhost/api/psb/image/'
        key = 'photo'
        value =[]
        newInfo = ManageKeys(info)
        for i in range( len(info) ):
            value.append(info[i]['imageId'])
        
        newInfo.Add( key , value, url, concatenate=True ) #add to any document in the list (photo : url + image resource)
        newInfo.PutId()                                  #add id to every document
        newInfo.Remove('imageId')
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
    

@app.route('/api/admin', methods = ['GET','POST'])
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
            pwd = client.hash_password( Adminpass )
            client.Save(Admincollection,username,pwd)
            return OK('user saved',201)
        else:
            return BAD('error','only can exists one admin',409)

    else:    
        client = ManagePsb(credentials,databaseName)
        cursor = client.Filter(collection)
        info = list(cursor)
        newInfo = ManageKeys(info)
        for data in info:
            data['_id'] = str( data['_id'] )

        return newInfo.LikeJson()

@app.route("/api/admin/<psb_id>", methods=['PUT','DELETE'])
def deletePsb(psb_id):
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





