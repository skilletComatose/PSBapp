import json
err1 = 'Error_with_image'

dataKey = "psb" # datakey is the json key where psb information's are (psb is a key in data dict     )

imageKey = "img" # imagekey is the key with image was posted


err3 = 'Image_error'

err4 = 'error'

err5 = 'auth_failed'

msg = 'Error with image : missing image'

msg1 = 'psb saved successfully!'

msg2 =  ['1. Field error :key posted not in dict'  , 
         '2. Image field was send empty o.O'       , 
         "3. neither image and key  weren't sent"]

msg3 = "key are ok but, the image wasn't sent :("


msg4 = {'json_error':'Key posted not in dict '}

msg5 = 'Warning'

msg6 = 'Missing'

msg7 = 'Image not found'

msg8 = 'bad request'

msg9 = 'user saved'

msg10 = 'only can exists one admin'

msg11 = 'incorrect id'

msg12 = 'updated'

msg13 = 'not updated'

msg14 = 'removed'

msg15 = 'not deleted because id not found'

msg16 = 'incorrect id'

msg17 = 'Username or Password are incorrect '

msg18 = 'Missing json '

msg19 = 'Missing  multipart/form-data'

warning = 'The psb sent is already registered, but thanks for send it'

auth_token = json.dumps( {"auth_token":"anytoken"} )

json_error = 'json_error'

blacklistName = 'blacklist'

logout1 = {'status':'logout'}
log_out = json.dumps(logout1)
missing_token = 'missing token'

token_expired = 'token in blacklist, please log again'

signature = 'Signature expired. Please log in again.'

auth_token_response = 'auth_token'
invalid_token = 'Invalid token. Please log in again.'
E400   = '1. '+ msg19        +'\n\n'+'2. '+str(msg4)      +'\n\n'+ '3. '+msg3 +'\n\n' + '4. '+str(msg2) + '\n\n' + '5. '+ '{ '+json_error +':'+msg18+' }'
E400v2 = '1. '+ msg18        +'\n\n'+'2. '+msg8
E400v3 = '1. '+ missing_token+'\n\n'+'2. '+msg18          +'\n\n'+'3. '+msg11 
E400v4 = '1. '+ msg18        +'\n\n'+'2. '+msg8           +'\n\n'+'3. '+msg17 
E403   = '1. '+ signature    +'\n\n'+'2. '+ invalid_token +'\n\n'+'3. '+token_expired
