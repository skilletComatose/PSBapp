from flask_restx import  fields,reqparse
from werkzeug.datastructures import FileStorage



psb_post_parameters = reqparse.RequestParser()
psb_post_parameters.add_argument('psb',required=True, location='form', help='json with psb data, example : {  "latitude":"any latitude", "longitude":"any longitude", "address":"any address", "neighborhood":"any neighborhood"} ')
psb_post_parameters.add_argument('img', type=FileStorage,required=True ,location='files',help='psb image')


admin_post = reqparse.RequestParser()
admin_post.add_argument('username', required=True,location='json')
admin_post.add_argument('password', required=True,location='json')

admin_get = reqparse.RequestParser()
admin_get.add_argument('Authorization', location='headers',help='json web token(jwt)')


admin_put = reqparse.RequestParser()
admin_put.add_argument('status',required=True, location='form',help='change psb status, example : {"status":"A"}')
admin_put.add_argument('Authorization', location='headers',help='json web token(jwt)')
