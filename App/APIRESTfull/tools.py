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

    
    def Validate(self):
        # complete returns true if all data is present 
        complete = (
            'longitude'    in self.Decode()  and
            'latitude'     in self.Decode()  and     
            'status'       in self.Decode()  and    
            'address'      in self.Decode()  and
            'neighborhood' in self.Decode()  
        )
        
        if(complete):
            return True
            
        else: # return False if any key is missing, also
              # searches for the missing key and adds it to a missing list 
              
            if('status' not in self.Decode()):  
                self.missing.append ('Missing psb status')
            
            if('address' not in self.Decode()):  
                self.missing.append ('Missing psb address')                

            if('neighborhood' not in self.Decode()):  
                self.missing.append ('Missing psb neighborhood')

            if('latitude' not in self.Decode()):  
                self.missing.append ('Missing psb latitude')       

            if('longitude' not in self.Decode()):  
                self.missing.append ('Missing psb longitude')

            return False


class SavePsb:
    def __init__(self,HostName,UserName,Password):
        self.login = Login(HostName,UserName,Password)
        self.db = None
    
    def Save(self,JsonToSave,DatabaseName,CollectionName,ImageName):
        self.imgId = ImageName
        self.json = JsonToSave
        self.db = self.login.Client()[DatabaseName]
        self.db[CollectionName].insert(
                                    {   
                                        'imageId':self.imgId                     ,
                                        'latitude':self.json['latitude']         ,
                                        'longitude':self.json['longitude']       ,
                                        'status':self.json['status']             ,
                                        'address':self.json['address']             ,
                                        'neighborhood':self.json['neighborhood'] ,
                                        'CreationDate':datetime.datetime.utcnow(),
                                        'LastUpdated': datetime.datetime.utcnow()
                                    }        
        
                                 )
        
class SaveImage:
    def __init__(self,ALLOWED_EXTENSIONS):
        self.ok = ALLOWED_EXTENSIONS
        self.name = None
    
    def Allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ok

    
    def Save(self,KeyName,AppConfig):
        if KeyName in request.files:
            file = request.files[ KeyName ]                
            
            if file and self.Allowed_file(file.filename):
                filename = secure_filename(file.filename)
                newName = ChangeName(filename)
                self.name = newName
                if(self.name != None and self.name != ''):
                    file.save(os.path.join(AppConfig, newName) )        
        else:
            return BAD( "error","keyname doen't are in the dict" )
        

def OK():
    return jsonify({'ok': True, 'message': 'psb saved successfully!'}), 200

def BAD(error,description):
    return jsonify({error:description}), 400                

def Point(string):
    for i in range( len(string) ):
        if(string[i]=="."):
            return i

def ChangeName(filename):
    x = datetime.datetime.now()
    header = ""
    date = str(x)
    x = Point(filename)
    extension="."
    
    for i in range(x):
        header += filename[i]
    
    for i in range(x+1,len(filename)):
        extension += filename[i]
    
    filename = header +"_"+date + extension
    return filename
