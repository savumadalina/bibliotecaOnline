import datetime
class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "Carti"

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q


	def reserve(self, user_id, book_id):
		# if not self.available(book_id):
		# 	return "err_out"
		print(user_id)
		print(book_id)
		q = self.db.query("INSERT INTO Rezervari (ID_Utilizator, ID_Carte, DataRezervare) VALUES('{}', '{}', '{}');".format(user_id, book_id, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
		
		self.db.query("UPDATE @table set Disponibilitate=0 where id={};".format(book_id))
		self.db.commit()

		return q

	def getBooksByUser(self, user_id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID left join Rezervari d on d.ID_Carte = a.id where d.ID_Utilizator={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getloanBooksByUser(self, user_id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID left join Imprumuturi d on d.ID_Carte = a.id where d.ID_Utilizator={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBooksCountByUser(self, user_id):
		q = self.db.query("select count(Rezervari.ID_Carte) as books_count from @table left join Rezervari on Rezervari.ID_Carte = @table.id where Rezervari.ID_Utilizator={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBook(self, id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID where a.id='{}'".format(id))

		book = q.fetchone()

		return book

	def getBookProfile(self,id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor,d.DataImprumut,d.DataReturnare,e.DataRezervare,f.Email from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID left join Imprumuturi d on a.ID=d.ID_Carte left join Rezervari e on a.ID=e.ID_Carte left join Utilizatori f on e.ID_Utilizator=f.ID or d.ID_Utilizator=f.ID where a.id='{}'".format(id))

		book = q.fetchone()

		return book

	def getBookAll(self, id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor,d.DataImprumut,d.DataReturnare,e.DataRezervare,f.Email from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID left join Imprumuturi d on a.ID=d.ID_Carte left join Rezervari e on a.ID=e.ID_Carte left join Utilizatori f on e.ID_Utilizator=f.ID or d.ID_Utilizator=f.ID where a.id='{}'".format(id))

		book = q.fetchone()

		return book

	# def available(self, id):
	# 	book = self.getById(id)
	# 	count = book['count']
	#
	# 	if count < 1:
	# 		return False
	#
	# 	return True

	def getById(self, id):
		q = self.db.query("select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID where a.id='{}'".format(id))

		book = q.fetchone()

		return book

	def list(self, availability=1):
		query="select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID where Disponibilitate=1"
		# Usually when no-admin user query for book
		# if availability==1: query= query+"  WHERE Disponibilitate={}".format(availability)
		
		books = self.db.query(query)
		
		books = books.fetchall()


		return books

	def listAll(self):
		query="select a.*, b.nume as Gen, c.nume as Autor,d.DataImprumut,d.DataReturnare,e.DataRezervare from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID left join Imprumuturi d on a.ID=d.ID_Carte left join Rezervari e on a.ID=e.ID_Carte"

		books = self.db.query(query)

		books = books.fetchall()

		return books

	def listLoans(self):
		query = "select a.*,b.ID_Utilizator,b.ID as ID_Rezervare,c.Email from @table a inner join Rezervari b on a.ID=b.ID_Carte inner join Utilizatori c on b.ID_Utilizator=c.ID"
		# Usually when no-admin user query for book
		# if availability==1: query= query+"  WHERE Disponibilitate={}".format(availability)

		books = self.db.query(query)

		books = books.fetchall()

		return books

	def loan(self, id_reservation):
		queryDetails = "select ID_Utilizator,ID_Carte from Rezervari where ID={}".format(id_reservation)
		details = self.db.query(queryDetails)

		details = details.fetchone()

		loanDate = datetime.datetime.now() + datetime.timedelta(days=14)
		queryLoans = "insert into imprumuturi (ID_Utilizator,ID_Carte,DataImprumut,DataReturnare) values ('{}','{}','{}','{}')".format(details['ID_Utilizator'],details['ID_Carte'],datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),loanDate.strftime('%Y-%m-%d %H:%M:%S'))
		print(queryLoans)
		queryReservations = "delete from rezervari where ID={}".format(id_reservation)

		loans=self.db.query(queryLoans)
		reservations=self.db.query(queryReservations)
		self.db.commit()

		return

	def getReserverdBooksByUser(self, user_id):
		query="select concat(ID_Carte,',') as user_books from Rezervari WHERE ID_Utilizator={}".format(user_id)
		
		books = self.db.query(query)
		
		books = books.fetchone()


		return books

	def search_book(self, name, availability=1):
		query="select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID where Titlu LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND Disponibilitate={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books

	def search_email(self, name, availability=1):
		query = "select a.*, b.nume as Gen, c.nume as Autor,e.Email from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID inner join Rezervari d on a.ID=d.ID_Carte inner join Utilizatori e on d.ID_Utilizator=e.ID where e.Email LIKE '%{}%' or a.Titlu LIKE '%{}%'".format(name,name)

		# Usually when no-admin user query for book
		if availability == 1: query = query + "  AND Disponibilitate={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()

		return books

	def filterByCriteria(self):
		queryGenres="select * from Genuri"
		queryAuthors="select * from Autori"

		genres = self.db.query(queryGenres)
		genres = genres.fetchall()
		authors = self.db.query(queryAuthors)
		authors = authors.fetchall()

		return genres, authors

	def templateFilters(self, filters):
		templateFilter = '('
		for i in filters:
			templateFilter += str(i) + ','
		templateFilter = templateFilter[:-1] + ')'

		return templateFilter

	def searchBookFilters(self, filters, keyword, genres, authors):

		queryKeyword = ''
		queryGenres = ''
		queryAuthors = ''
		if keyword != '':
			queryKeyword = "Titlu like '%{}%'".format(keyword)
		templateGenres = self.templateFilters(genres)
		templateAuthors = self.templateFilters(authors)
		if templateGenres != ')':
			queryGenres = "b.ID in " + templateGenres
		if templateAuthors != ')':
			queryAuthors = "c.ID in " + templateAuthors
		queries = [queryKeyword,queryGenres,queryAuthors]
		query = "select a.*, b.nume as Gen, c.nume as Autor from @table a inner join Genuri b on a.ID_Genuri=b.ID inner join Autori c on a.ID_Autori=c.ID where "
		count = 0
		countTrue = 0
		for i in filters:
			if i:
				if countTrue > 0:
					query += " and "
				query += queries[count]
				countTrue += 1
			count += 1
		query += " and Disponibilitate=1"
		q = self.db.query(query)
		books = q.fetchall()

		return books

	def addBook(self, title, author, genre, pg, language, image):

		queryAuthor = "select ID from Autori where Nume = '{}'".format(author)
		queryGenre = "select ID from Genuri where Nume = '{}'".format(genre)

		authors = self.db.query(queryAuthor)
		authors = authors.fetchone()
		genres = self.db.query(queryGenre)
		genres = genres.fetchone()

		query = "insert into @table (Titlu, Disponibilitate, PG, Limba, ID_Genuri, ID_Autori, Imagine) values ('{}',1,'{}','{}','{}','{}','{}')".format(title,pg,language,authors['ID'], genres['ID'], image)
		add = self.db.query(query)
		self.db.commit()
		return