from flask import Flask,request
from tools import ReadJson,SavePsb,OK,BAD,Empty,SaveImage
#from App.APIRESTfull.tools import ReadJson,SavePsb,OK,BAD,Empty,SaveImage

UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

folder = app.config['UPLOAD_FOLDER']

err1 = "error with image "
err2 = "key posted not in dict :("
msg = {"error with image":"missing image"}
msg2 =  "Field error :key posted not in dict OR  image field was send empty o.O"
           
# i have to validate database haven't duplicate data 

@app.route("/api/v1/psb", methods=['GET', 'POST'])
def psbPost():
    data = request.form.to_dict() #data is a dict with multipart/form-data
    dataKey = "psb"
    imageKey ="img"   
    
    if( request.method == "POST" and data ):
        if dataKey not in data :
            return BAD( "error with json file ",err2)
        
        Json = ReadJson(data[dataKey]) #datakey is the json key where psb informations are (psb is a key in data dict     )
        if( Json.Validate() ):
            img = SaveImage( ALLOWED_EXTENSIONS ) 
            media = request.files
            if(imageKey not in media and imageKey in data ):
                return BAD( err1, "key are ok but, the image wasn't sent :(" )
                
            if(imageKey not in media):
                return BAD (err1, msg2 )      
            
            img.Save( imageKey, folder ) # imagekey is the key with image was posted
            ImageId = img.name
            if( ImageId != None and ImageId != " " ):
                client = SavePsb( "mongo", "root", "pass" )
                client.Save( Json.Decode(),"psb_data","psbCollec", img.name )
            else:
                return BAD( err1, msg ) 
            
            
            return OK()
        
        else:
            return BAD( "error" ,Json.missing )
    

    


#    if 'file' in request.files:
#        file = request.files['file']
#
#    if file.filename == '':
#        return BAD( {"error":"Missing image"} )
#
#    if file and allowed_file(file.filename):
#        filename = secure_filename(file.filename)
#        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#        return 'uploaded_file',filename
