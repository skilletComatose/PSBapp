from pymongo import MongoClient

class Login:
    def __init__(self,HostName,UserName,Password):
        self.host = HostName
        self.user = UserName
        self.password = Password
    
    def Client(self):
        client = MongoClient( self.host, username =self.user, password = self.password )
        return client