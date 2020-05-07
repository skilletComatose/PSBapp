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
            
            if('address' not in self.Decode()):  
                self.missing.append ('Missing psb address')                

            if('neighborhood' not in self.Decode()):  
                self.missing.append ('Missing psb neighborhood')

            if('latitude' not in self.Decode()):  
                self.missing.append ('Missing psb latitude')       

            if('longitude' not in self.Decode()):  
                self.missing.append ('Missing psb longitude')

            return False


class ManagePsb:
    def __init__(self,HostName,UserName,Password,DatabaseName):
        self.login = Login(HostName,UserName,Password)
        self.db = self.login.Client()[DatabaseName]
    

    
    def Filter(self,DictToValidate,Collection_Where_Filter_WillDo, Condition_To_DoTheFilter,Projection=None):
       query = Condition_To_DoTheFilter
       self.db
       if(Projection):
            fil = self.db[Collection_Where_Filter_WillDo].find( query, Projection)
       else:      
            fil = self.db[Collection_Where_Filter_WillDo].find(query)
       return fil
        
#    def Update(self,DataToUpdate,WhereUpdate,Collection_Where_Update):
#        self.db


    def Save(self,JsonToSave,CollectionName,ImageName):
        self.imgId = ImageName
        self.json = JsonToSave
        self.db[CollectionName].insert(
                                    {   
                                        'imageId':self.imgId                     ,
                                        'latitude':self.json['latitude']         ,
                                        'longitude':self.json['longitude']       ,
                                        'status':'none'                              ,
                                        'address':self.json['address']           ,
                                        'neighborhood':self.json['neighborhood'] ,
                                        'CreationDate':datetime.datetime.utcnow(),
                                        'LastUpdated': datetime.datetime.utcnow()
                                    }        
        
                                 )
        
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
    x = Point(filename)
    extension="."
    
    for i in range(x):
        header += filename[i]
    
    for i in range(x+1,len(filename)):
        extension += filename[i]
    
    filename = header +"_"+date + extension
    return filename
