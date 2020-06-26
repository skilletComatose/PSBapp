import json
import datetime
import os
import pymongo
from flask import jsonify ,request
from database import Login 
from werkzeug.utils import secure_filename
import jwt
import bcrypt
from config import salt,credentials,adminDatabase,Admincollection
from msg import missing_token, token_expired,invalid_token,signature

                 
class ReadJson: #read a Json object, turns it into a string and then into a dictionary
    def __init__(self,json_data):
        self.json = json_data
        self.missing = []
    
    def Decode(self):
        try:
            data = json.loads(self.json)
        except:
            return False
        return data

    def Validate(self,JsonToValidate):
        # complete returns true if all data is present         
        longitude    = None
        latitude     = None
        address      = None
        neighborhood = None

        complete = (
            'longitude'    in JsonToValidate   and
            'latitude'     in JsonToValidate   and
            'address'      in JsonToValidate   and
            'neighborhood' in JsonToValidate    
        )
        
        if(complete):
            longitude      = not JsonToValidate['longitude'].strip() #return true if string is empty
            latitude       = not JsonToValidate['latitude'].strip()
            address        = not JsonToValidate['address'].strip() 
            neighborhood   = not JsonToValidate['neighborhood'].strip()
            if(longitude):
                self.missing.append('longitude is empty')
                return False

            if(latitude):
                self.missing.append('latitude is empty')
                return False
            
            if(address):
                self.missing.append('address is empty')
                return False
            
            if(neighborhood ):
                self.missing.append('neighborhood is empty')   
                return False                                 
                                                
            return True
            
        else: # return False if any key is missing, also
              # searches for the missing key and adds it to a missing list 
            
            if('address' not in JsonToValidate):  
                self.missing.append ('Missing psb address')                            

            if('neighborhood' not in JsonToValidate):  
                self.missing.append ('Missing psb neighborhood')

            if('latitude' not in JsonToValidate):  
                self.missing.append ('Missing psb latitude')       

            if('longitude' not in JsonToValidate):  
                self.missing.append ('Missing psb longitude')
            
            return False


class Admin_ReadJson(ReadJson):    
    def Decode(self):
        data = json.dumps(self.json)
        data2 = json.loads(data)
        return data2

    def Validate(self,JsonToValidate):
        complete = ('status' in JsonToValidate )    
        if(complete):
            return True
            
        else: # return False if any key is missing, also
              # searches for the missing key and adds it to a missing list                 

            if('status' not in JsonToValidate):  
                self.missing.append ('Missing psb status')

            return False

    def Status(self,data):
        d = data['status']
        statusList = ['A','a','I','i','V','v']
        ok = (d in statusList)    
        if(not ok):
            m = "status must be A or I or V,  not "
            m += d
            self.missing.append( m )
        return ok

class ManagePsb:
    def __init__(self, connectionString, DatabaseName):
        self.login = Login(connectionString)
        self.db = self.login.Client()[DatabaseName]
      
    def Filter(self,Collection, query=None,Key=None,Value=None,Operator=None,Projection=None):
        #query in the conndition to do the filter
        #projection is a data filter, to don't return all data 
       if(Projection and query):
            fil = self.db[Collection].find( query, Projection)
       
       if(Projection and Key and Value and Operator ):
           fil = self.db[Collection].find({ Key : { Operator:Value } } , Projection)
       
       if(query is None and Key is None ):      
            fil = self.db[Collection].find({},Projection)
       
       if(Projection is None and query is None):
           fil = fil = self.db[Collection].find()
       return fil
        
    def Update(self,CollectionName,query,Change):
        Change['LastUpdated'] = datetime.datetime.utcnow()
        result = self.db[CollectionName].update_one( query, { "$set" : Change })
        if (result.matched_count > 0):
            return True 
        else:
            return False
    def Delete(self,CollectionName,query):
        a = self.db[CollectionName].count()
        self.db[CollectionName].remove(query)
        b = self.db[CollectionName].count()
        if(a > b):
            return True
        else:
            return False
    def Save(self,JsonToSave,CollectionName,ImageName):
        self.imgId = ImageName
        self.json = JsonToSave
        self.db[CollectionName].insert(
                                         {   
                                           'imageId':self.imgId                     ,
                                           'latitude':self.json['latitude']         ,
                                           'longitude':self.json['longitude']       ,
                                           'status':'V'                             ,
                                           'address':self.json['address']           ,
                                           'neighborhood':self.json['neighborhood'] ,
                                           'CreationDate':datetime.datetime.utcnow(),
                                           'LastUpdated': datetime.datetime.utcnow()
                                         }        
        
                                      )



class admin(ManagePsb):
    
    def hash_password(self, password,SECRET_KEY):
        a = password
        b = SECRET_KEY
        a = str(a) + str(b)
        a = a.encode()
        phash = bcrypt.hashpw( a, salt )
        self.password_hash = phash
        return self.password_hash

    def check_hash(self,password,hash_toCheck,SECRET_KEY):
        password += SECRET_KEY
        password = password.encode()
        if (bcrypt.checkpw( password, hash_toCheck )):
            return True
        else:
            return False
    
    def encode_auth_token(self,username,SECRET_KEY):
        try:
            payload = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),# exp: expiration date of the token
                        'iat': datetime.datetime.utcnow(),# iat: the time the token is generated
                        'sub': username # sub: the subject of the token (the user whom it identifies)
                    }
            return jwt.encode(
                                payload,
                                SECRET_KEY,
                                algorithm='HS256'
                             )
            
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(token,SECRET_KEY):
        try:
            payload = jwt.decode(token, SECRET_KEY )
            resp = [True,payload['sub'],200]
            return resp
        
        except jwt.ExpiredSignatureError:
            resp = [False,signature,403]   
            return resp
        
        except jwt.InvalidTokenError: 
            resp = [False,invalid_token,403]
            return resp                

    
    def Save(self,CollectionName,username, password_hash):
        self.db[CollectionName].insert(
                                        {
                                        'username':username,
                                        'password':password_hash
                                        }
                                      )

    def Black_list(self,CollectionName,token):
        self.db[CollectionName].insert(token)

                                      

class ManageKeys: #to do operations in  dics list
    def __init__(self,Lis_Of_dict):
        self.list = Lis_Of_dict        

    def Add(self,key,value,Data_To_concatenate = None,concatenate=False):
        if(concatenate and Data_To_concatenate):
            i = 0
            base = Data_To_concatenate
            for data in self.list :
                data[key] =  base + value[i]
                i += 1 
        
        else:
            i = 0       
            for data in self.list :
                data[key] = value[i]
                i += 1

    def Remove(self,key):
        for data in self.list :
            del data[key]

    def PutId(self,Id=None,progress=None):
        if(progress and Id):
            for anydata in self.list:
                anydata['id'] = Id
                Id += progress
        else:
            Id = 1
            for anydata in self.list:
                anydata['id'] = Id
                Id += 1

    
    def LikeJson(self):
        return jsonify (self.list)



class SaveImage:
    def __init__(self,ALLOWED_EXTENSIONS):
        self.ok = ALLOWED_EXTENSIONS
        self.name = None
        self.file = None
        self.conf = None
    
    
    def Allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ok

    
    def Save(self,KeyName,AppConfig):
        if KeyName in request.files:
            file = request.files[ KeyName ]                
            self.file = file
            self.conf = AppConfig
            if file and self.Allowed_file(file.filename):
                filename = secure_filename(file.filename)
                newName = ChangeName(filename)
                self.name = newName


    def Upload(self):            
        if(self.name is not None):
            self.file.save(os.path.join(self.conf, self.name) )        
                



def check_token(SECRET_KEY):
    auth_token = request.headers.get('Authorization')
    if(auth_token):
        client = admin(credentials,adminDatabase )
        query = {'token':auth_token}
        projec = {'_id':0}
        cursor = client.Filter('blacklist',query=query,Projection=projec)
        c = cursor.count()
        if(c == 1):   
            resp = [False,token_expired,403,auth_token]
            return resp
        resp = admin.decode_auth_token(auth_token,SECRET_KEY)
        resp.append(auth_token)
        return resp
    else:
        resp = [False,missing_token,400]
        return resp


def OK(message,responsecode):
    return jsonify(message), responsecode

def BAD(error,description,ResponseCode):
    return jsonify({error:description}), ResponseCode                

def Point(string):
    for i in range( len(string) ):
        if(string[i]=="."):
            return i
def check_image(path,imagename):
    return os.path.exists(path + '/' + imagename) 

def remove_img(path,imagename):
    os.remove(path + '/' + imagename)

                     

def ChangeName(filename):
    x =  datetime.datetime.utcnow()
    header = ""
    date = str(x)
    date = date.replace(" ","_")
    x = Point(filename)
    extension="."
    
    for i in range(x):
        header += filename[i]
    
    for i in range(x+1,len(filename)):
        extension += filename[i]
    
    filename = header +"_"+date + extension
    return filename
