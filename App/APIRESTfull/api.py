from flask import Flask,request,jsonify 
#from App.APIRESTfull.client import client
#from App.APIRESTfull.tools import ReadJson
from client import client
from tools import ReadJson
app = Flask(__name__)


# i have to validate database haven't duplicate data 
@app.route("/api/v1/psb", methods=['GET', 'POST'])
def psbPost():
    json = request.get_json()
    if(request.method == "POST" and json):
        data = ReadJson(json)
       
        if(data.Validate()):
            #with client:
            #    db = client.psb_data
            #    db.psb.insert( data.Decode() )
                return jsonify({'ok': True, 'message': 'psb saved successfully!'}), 200
        
        else:
            return jsonify({"Data Missing ":data.missing}), 400

    else:
        return jsonify({"error":"Json empty"}), 400

    


