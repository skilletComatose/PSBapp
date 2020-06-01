import json
import datetime
import os
import pymongo
from flask import jsonify ,request
from database import Login
from werkzeug.utils import secure_filename
from passlib.apps import custom_app_context as pwd_context
#from App.APIRESTful.database import Login

                 
class ReadJson: #read a Json object, turns it into a string and then into a dictionary
    def __init__(self,json_data):
        self.json = json_data
        self.missing = []
    
    def Decode(self):
        data = json.loads(self.json)
        return data

    def Validate(self,JsonToValidate):
        # complete returns true if all data is present 
        longitude      = not JsonToValidate['longitude'].strip() #return true if string is empty
        latitude       = not JsonToValidate['latitude'].strip()
        address        = not JsonToValidate['address'].strip() 
        neighborhood   = not JsonToValidate['neighborhood'].strip()
        
        complete = (
            'longitude'    in JsonToValidate  and not longitude     and
            'latitude'     in JsonToValidate  and not latitude      and
            'address'      in JsonToValidate  and not  address      and
            'neighborhood' in JsonToValidate  and not neighborhood  
        )
        
        if(complete):
            
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
            
            if(longitude):
                self.missing.append('longitude is empty')

            if(latitude):
                self.missing.append('latitude is empty')

            if(address):
                self.missing.append('address is empty')

            if(neighborhood ):
                self.missing.append('neighborhood is empty')   

            return False


class Admin_ReadJson(ReadJson):    
    def Decode(self):
        data = json.dumps(self.json)
        data2 = json.loads(data)
        return data2

    def Validate(self,JsonToValidate):
        # complete returns true if all data is present 
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
        ok = (
                d in statusList
             )
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
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def Save(self,CollectionName,username, password_hash):
        self.db[CollectionName].insert(
                                        {
                                        'username':username,
                                        'password':password_hash
                                        }
                                      )



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
        if(self.name != None and self.name != ''):
            self.file.save(os.path.join(self.conf, self.name) )        
                






def OK(message,responsecode):
    return jsonify({'ok': message}), responsecode

def BAD(error,description,ResponseCode):
    return jsonify({error:description}), ResponseCode                

def Point(string):
    for i in range( len(string) ):
        if(string[i]=="."):
            return i
            
    

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
