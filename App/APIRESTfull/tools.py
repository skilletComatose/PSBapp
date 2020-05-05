import json
from flask import jsonify 
from database import Login
import pymongo
import datetime
#from App.APIRESTfull.database import Login


class ReadJson:
    #read a Json object, turns it into a string and then into a dictionary 
    def __init__(self,json_data):
        self.json = json_data
        self.missing = []
    def Decode(self):
        data = json.dumps(self.json)
        data2 = json.loads(data)
        return data2  
    
    def Validate(self):
        # complete returns true if all data is present 
        complete = (
            'longitude'  in self.Decode()  and
            'latitude'  in self.Decode()  and  
            'imageId'      in self.Decode()  and   
            'status'       in self.Decode()  and    
            'addres'    in self.Decode()  and
            'neighborhood' in self.Decode()  
        )
        
        if(complete):
            return True
            
        else: # return False if any key is missing, also
              # searches for the missing key and adds it to a missing list 
              
            if('imageId' not in self.Decode()):  
                self.missing.append ('Missing psb image')       

            if('status' not in self.Decode()):  
                self.missing.append ('Missing psb status')
            
            if('addres' not in self.Decode()):  
                self.missing.append ('Missing psb addres')                

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
    
    def Save(self,JsonToSave,DatabaseName,CollectionName):
        self.json = JsonToSave
        self.db = self.login.Client()[DatabaseName]
        self.db[CollectionName].insert(
                                    {   
                                        'imageId':self.json['imageId'],
                                        'latitude':self.json['latitude'],
                                        'longitude':self.json['longitude'],
                                        'status':self.json['status'],
                                        'addres':self.json['addres'],
                                        'neighborhood':self.json['neighborhood'],
                                        'CreationDate':datetime.datetime.utcnow() ,
                                        'LastUpdated': datetime.datetime.utcnow()
                                    }        
        
                                 )
        
        

def OK():
    return jsonify({'ok': True, 'message': 'psb saved successfully!'}), 200
def BAD(x):
    return jsonify({"Data Missing ":x}), 400                
def Empty():    
    return jsonify({"error":"Json empty"}), 400           
  
                    
            

