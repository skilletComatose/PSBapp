import json

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
        else:
            
            if('imageId' not in self.Decode()):  
                self.missing.append ('Missing psb image')       

            if('status' not in self.Decode()):  
                self.missing.append ('status')
            
            if('addres' not in self.Decode()):  
                self.missing.append ('Missing psb addres')                

            if('neighborhood' not in self.Decode()):  
                self.missing.append ('Missing psb neighborhood')

            if('latitude' not in self.Decode()):  
                self.missing.append ('Missing psb latitude')       

            if('longitude' not in self.Decode()):  
                self.missing.append ('Missing psb longitude')

            return False



                 
            
  
                    
            

