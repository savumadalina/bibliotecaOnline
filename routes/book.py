from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO

from Controllers.UserManager import UserManager
from Controllers.BookManager import BookManager

book_view = Blueprint('book_routes', __name__, template_folder='/templates')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)

@book_view.route('/books/', defaults={'id': None})
@book_view.route('/books/<int:id>')
def home(id):
	user_manager.user.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)

		print('----------------------------')
		print(b)

		return render_template("book_view.html", books=b, g=g)
	else:
		b = book_manager.list()
		genres, authors = book_manager.getFilters()
		user_books=[]
		if user_manager.user.isLoggedIn():
			reserved_books = book_manager.getReserverdBooksByUser(user_id=user_manager.user.uid())
			
			if reserved_books is not None:
				user_books = reserved_books['user_books'].split(',')
		
		print("---------------------------------------")
		print(user_books)

		if b and len(b) <1:
			return render_template('books.html', error="No books found!")
	
		return render_template("books.html", filtersButton=True, books=b, g=g, user_books=user_books, genres=genres, authors=authors)


	return render_template("books.html", books=b, g=g)


@book_view.route('/books/add/<id>', methods=['GET'])
@user_manager.user.login_required
def add(id):
	user_id = user_manager.user.uid()
	book_manager.reserve(user_id, id)

	b = book_manager.list()
	user_manager.user.set_session(session, g)
	
	return render_template("books.html", msg="Book reserved", books=b, g=g)

@book_view.route('/books/search', methods=['GET'])
def searchFilters():
	user_manager.user.set_session(session, g)
	filters=[]
	b = book_manager.list()
	genresHTML, authorsHTML = book_manager.getFilters()
	if "keyword" in request.args and request.args["keyword"] == '' and "genres[]" not in request.args and "authors[]" not in request.args:
		return render_template("books.html", filters=True, books=b, genres=genresHTML, authors=authorsHTML)
	if "keyword" not in request.args and request.args["keyword"] != '' and "genres[]" not in request.args and "authors[]" not in request.args:
		return render_template("search.html")
	if "keyword" in request.args and request.args["keyword"] != '':
		filters.append(True)
		keyword = request.args["keyword"]
	else:
		filters.append(False)
		keyword = ''
	# if len(keyword)<1:
	# 	return redirect('/books')
	if "genres[]" in request.args:
		filters.append(True)
		genres = request.args.getlist('genres[]')
	else:
		filters.append(False)
		genres = []
	if "authors[]" in request.args:
		filters.append(True)
		authors = request.args.getlist('authors[]')
	else:
		filters.append(False)
		authors = []
	d = book_manager.searchFilters(filters,keyword,genres,authors)

	if len(d) >0:
		return render_template("books.html", filtersButton=True, search=True, books=d, count=len(d), g=g, genres=genresHTML,authors=authorsHTML)
	return render_template('books.html', filtersButton=True, error="Nici o carte găsită!")


@book_view.route('/books/profile/<int:id>')
def bookProfile(id):
	user_manager.user.set_session(session, g)

	if id != None:
		b = book_manager.getBookProfile(id)

		return render_template("book_view_profile.html", books=b, g=g)
	b = book_manager.list()
	return render_template("books.html", books=b, g=g)

