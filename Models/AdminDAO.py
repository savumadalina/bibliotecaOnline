class AdminDAO():
	db = {}
	
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "Utilizatori"

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where email='{}' and Rol='Bibliotecar'".format(email))

		user = q.fetchone()

		return user
