

class user:
	password_hash = db.Column(db.String(128))
	
	def __init__(this, username, password, userPerms=UserPermission):
	
