import json
data="{  \"longitude\":\"any\",  \"latitude\": \"any\",  \"imageId\": \"2\",  \"status\" : \"W\",  \"addres\": \"gaviotas Cll 23 kr \",  \"neighborhood\": \"las gaviotas\"}"


#dumps the json object into an element
#json_str = json.dumps(data)
#print("\ndumps",json_str)
#print(type(json_str))
#load the json to a string
#resp = json.loads(data)
#print("\n\nloads",resp)
#print(type(resp),resp['longitude'])
#p = resp.keys()
#print(p)
class ReadJson:
    def __init__(self,json_data):
        self.json = json_data
    def Decode(self):
        #data = json.dumps(self.json)
        data = json.loads(self.json)
        return data  
    
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
p = ReadJson(data)
q = p.Decode()
print(q['status'])
#//extract an element in the response