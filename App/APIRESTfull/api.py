from flask import Flask,request
from tools import ReadJson,ManagePsb,OK,BAD,SaveImage
#from App.APIRESTfull.tools import ReadJson,ManagePsb,OK,BAD,SaveImage

UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

folder = app.config['UPLOAD_FOLDER']

host = "mongo"
user = "root"
collection = "psbCollec"
password = "pass"
databaseName = "psb_data"

err1 = "Error with image : "
err3 = "Image error >>> Possible errors"
msg = " Error with image : missing image  "
msg2 =  ["1. Field error :key posted not in dict"  , 
         "2. Image field was send empty o.O"       , 
         "3. neither image and key  weren't sent"]
msg3 = "key are ok but, the image wasn't sent :("
msg4 = "Key posted not in dict :("
warning = "The psb sent is already registered, but thanks for send it"
# i have to validate database haven't duplicate data 

@app.route("/api/psb", methods=['GET', 'POST'])
def psbPost():
    data = request.form.to_dict() #data is a dict with multipart/form-data
    dataKey = "psb"
    imageKey ="img"   
    
    if( request.method == "POST" and data ):
        if dataKey not in data :
            return BAD( "error with json file ", msg4, 400)
        
        Json = ReadJson(data[dataKey]) #datakey is the json key where psb informations are (psb is a key in data dict     )
        if( Json.Validate() ):
            img = SaveImage( ALLOWED_EXTENSIONS ) 
            media = request.files
            if(imageKey not in media and imageKey in data ):
                return BAD( err1, msg3 , 400)
                
            if(imageKey not in media):
                return BAD (err3, msg2, 400 )      
            
            img.Save( imageKey, folder ) # imagekey is the key with image was posted
            ImageId = img.name
            if( ImageId != None and ImageId != " " ):
                client = ManagePsb( host, user,password,databaseName )
                dictionary = Json.Decode()
                query = {
                            "latitude":dictionary["latitude"],
                            "longitude":dictionary["longitude"]
                        }
                        
                cursor = client.Filter( dictionary, query, collection ) 
                c = cursor.count()
                if( c == 0 ):  
                   client.Save( Json.Decode(),collection, img.name )
                
                else:
                   return BAD ("Warning",warning,400)                
            else:
                return BAD( err1, msg ,400) 
            
            
            return OK()
        
        else:
            return BAD( "error" ,Json.missing, 400 )
    

