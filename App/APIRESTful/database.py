from pymongo import MongoClient



#this login is to work with Mongo Atlas
class Login:
    def __init__(self,connectionString):
        self.log = connectionString
       
    
    def Client(self):
        client = MongoClient( self.log )
        return client



# this Login class is to work with local mongodb
#class Login:
#    def __init__(self,HostName,UserName,Password):
#        self.host = HostName
#        self.user = UserName
#        self.password = Password
#    
#    def Client(self):
#        client = MongoClient( self.host, username =self.user, password = self.password )
#        return client