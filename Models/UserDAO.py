class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "Utilizatori"


	def list(self):
		users = self.db.query("select @table.id,@table.Nume,@table.Email,@table.Rol from @table").fetchall()

		return users

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where Email='{}'".format(email))

		user = q.fetchone()

		return user

	def add(self, user):
		name = user['Nume']
		email = user['Email']
		password = user['Parola']

		q = self.db.query("INSERT INTO @table (Nume, Email, Parola, Rol) VALUES('{}', '{}', '{}', '{}');".format(name, email, password, "Client"))
		self.db.commit()
		
		return q


	def update(self, user, _id):
		name = user['Nume']
		email = user['Email']
		password = user['Parola']
		q = self.db.query("UPDATE @table SET Nume = '{}', Email='{}', Parola='{}' WHERE id={}".format(name, email, password, _id))
		self.db.commit()
		
		return q
