from flask_restx import  fields,reqparse
from werkzeug.datastructures import FileStorage



psb_post_parameters = reqparse.RequestParser()
psb_post_parameters.add_argument('psb',required=True, location='form', help='json with psb data')
psb_post_parameters.add_argument('img', type=FileStorage,required=True ,location='files',help='psb image')


admin_post = reqparse.RequestParser()
admin_post.add_argument('username', required=True,location='json')
admin_post.add_argument('password', required=True,location='json')

admin_get = reqparse.RequestParser()
admin_get.add_argument('Authorization', location='headers',help='json web token(jwt)')