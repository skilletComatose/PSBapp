import json
data={
  "id": 0,
  "coordinates": "[51.508, -0.11]",
  "imageId": "string",
  "active": "true",
  "CreationDate": "[ 02, 03, 2020]",
  "LastUpdated": "[12 ,12 ,2020] ",
  #"direction": "string",
  "neighborhood": "string"
}

#dumps the json object into an element
json_str = json.dumps(data)

#load the json to a string
resp = json.loads(json_str)

class ReadJson:
    def __init__(self,json_data):
        self.json = json_data
    def Decode(self):
        data = json.dumps(self.json)
        data2 = json.loads(data)
        return data2  
    
    def Validate(self):
        return('id'        in self.Decode()  and  
            'coordinates'  in self.Decode()  and
            'imageId'      in self.Decode()  and   
            'active'       in self.Decode()  and    
            'CreationDate' in self.Decode()  and          
            'LastUpdated'  in self.Decode()  and
            'direction'    in self.Decode()  and
            'neighborhood' in self.Decode()  
        )
#print the resp
r = ReadJson(data)
if( r.Validate() ):
    print("positivo")

print(r.Validate())
#//extract an element in the response