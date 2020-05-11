import json
import datetime
import os
import pymongo
from flask import jsonify ,request
from database import Login
from werkzeug.utils import secure_filename
#from App.APIRESTfull.database import Login

class ReadJson:
    #read a Json object, turns it into a string and then into a dictionary 
    def __init__(self,json_data):
        self.json = json_data
        self.missing = []
    def Decode(self):
        data = json.loads(self.json)
        return data

    
    def Validate(self,JsonToValidate):
        # complete returns true if all data is present 
        complete = (
            'longitude'    in JsonToValidate  and
            'latitude'     in JsonToValidate  and       
            'address'      in JsonToValidate  and
            'neighborhood' in JsonToValidate  
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

            return False


class ManagePsb:
    def __init__(self,HostName,UserName,Password,DatabaseName):
        self.login = Login(HostName,UserName,Password)
        self.db = self.login.Client()[DatabaseName]
        self.database = DatabaseName
    

    
    def Filter(self,Collection, query=None,Key=None,Value=None,Operator=None,Projection=None):
        #query in the conndition to do the filter
        #projection is a data filter, to don't return all data 
       if(Projection and query):
            fil = self.db[Collection].find( query, Projection)
       
       if(Projection and Key and Value and Operator ):
           fil = self.db[Collection].find({ Key : { Operator:Value } } , Projection)
       
       if(query==None):      
            fil = self.db[Collection].find({},Projection)
       return fil
        
    def Update(self,CollectionName,DataToUpdate,query,Change):
        result = self.db[CollectionName].update( query, { "$set" : Change })
        if (result.modified_count > 0): 
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
                                        'status':'V'                              ,
                                        'address':self.json['address']           ,
                                        'neighborhood':self.json['neighborhood'] ,
                                        'CreationDate':datetime.datetime.utcnow(),
                                        'LastUpdated': datetime.datetime.utcnow()
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
            for data in self.list :
                data[key] = value

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
                

def OK():
    return jsonify({'ok': True, 'message': 'psb saved successfully!'}), 200

def BAD(error,description,ResponseCode):
    return jsonify({error:description}), ResponseCode                

def Point(string):
    for i in range( len(string) ):
        if(string[i]=="."):
            return i
            
    

def ChangeName(filename):
    x = datetime.datetime.now()
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
