import json

class ReadJson:
    #read a Json object, turns it into a string and then into a dictionary 
    def __init__(self,json_data):
        self.json = json_data
    def Decode(self):
        data = json.dumps(self.json)
        data2 = json.loads(data)
        return data2  
    
    def Validate(self):
        #return True if keys are in Json else false
        return('id'        in self.Decode()  and  
            'coordinates'  in self.Decode()  and
            'imageId'      in self.Decode()  and   
            'active'       in self.Decode()  and    
            'CreationDate' in self.Decode()  and          
            'LastUpdated'  in self.Decode()  and
            'direction'    in self.Decode()  and
            'neighborhood' in self.Decode()  
        )

