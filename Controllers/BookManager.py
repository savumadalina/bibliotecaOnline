from App.Books import Books

class BookManager():
	def __init__(self, DAO):
		self.misc = Books(DAO.db.book)
		self.dao = self.misc.dao

	def list(self, availability=1,user_id=None):
		if user_id!= None:
			book_list = self.dao.listByUser(user_id)
		else:
			book_list = self.dao.list(availability)

		return book_list

	def listAll(self):

		book_list = self.dao.listAll()

		return book_list

	def listLoans(self, user_id=None):
		book_list = self.dao.listLoans()

		return book_list

	def loan(self, id_reservation):
		self.dao.loan(id_reservation)
		return

	def getReserverdBooksByUser(self, user_id):
		books = self.dao.getReserverdBooksByUser(user_id)

		return books

	def getBook(self, id):
		books = self.dao.getBook(id)

		return books

	def getBookProfile(self, id):
		books = self.dao.getBookProfile(id)

		return books

	def getBookAll(self, id):
		books = self.dao.getBookAll(id)

		return books

	def search(self, keyword, availability=1):
		books = self.dao.search_book(keyword, availability)

		return books

	def searchEmail(self, keyword, availability=1):
		books = self.dao.search_email(keyword, availability)

		return books

	def getFilters(self):
		genres, authors = self.dao.filterByCriteria()

		return genres, authors

	def searchFilters(self, filters, keyword, genres, authors):
		books = self.dao.searchBookFilters(filters, keyword, genres, authors)

		return books


	def reserve(self, user_id, book_id):
		books = self.dao.reserve(user_id, book_id)

		return books

	def getUserBooks(self, user_id):
		books = self.dao.getBooksByUser(user_id)

		return books

	def getUserBooksCount(self, user_id):
		books = self.dao.getBooksCountByUser(user_id)

		return books

	def delete(self, id):
		self.dao.delete(id)

	def addBook(self, title, author, genre, pg, language, image):
		self.dao.addBook(title, author, genre, pg, language, image)