from flask import Flask,request
#from App.APIRESTfull.tools import ReadJson,SavePsb,OK,BAD,Empty
from tools import ReadJson,SavePsb,OK,BAD,Empty
app = Flask(__name__)


# i have to validate database haven't duplicate data 
@app.route("/api/v1/psb", methods=['GET', 'POST'])
def psbPost():
    data = request.get_json()
    if( request.method == "POST" and data ):
        Json = ReadJson(data)
       
        if( Json.Validate() ):
            client = SavePsb( "mongo", "root", "pass" )
            client.Save( Json.Decode(),"psb_data","psb" )
            return OK()
        
        else:
            return BAD( Json.missing )

    else:
        return Empty()

    


