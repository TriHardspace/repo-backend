from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

# When a user object is created, make sure that good (SAFE) data is used to create the user, or major issues will arise!
class user(Base):
    __tablename__ = "users"
    username = Column(String(64), primary_key=True)
    password = Column(String(128))
    email = Column(String(355))
    permissionLevel = Column(String(14))
    token = Column(String(128))
    def getToken():
      return self.token
    
    def getPassword():
        return self.password
    
    def getPermissionLevel():
        return self.permissionLevel
    
    def getEmail():
        return self.email
    
    def getUsername():
        return self.username

    def __repr__(self):
	    return f"username = {username}, password = {password}, email = {email}, permissionLevel = {permissionLevel}"

	
