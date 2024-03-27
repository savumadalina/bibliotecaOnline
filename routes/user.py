from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Misc.functions import *

from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["Email"])
		password = str(_form["Parola"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email și parola sunt obligatorii!")

		d = user_manager.signin(email, hash(password))

		if d and len(d)>0:
			session['user'] = int(d['ID'])

			return redirect("/")

		return render_template('signin.html', error="Email sau parolă incorecte!")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
	if request.method == 'POST':
		name = request.form.get('Nume')
		email = request.form.get('Email')
		password = request.form.get('Parola')

		if len(name) < 1 or len(email)<1 or len(password)<1:
			return render_template('signup.html', error="Toate câmpurile sunt obligatorii!")

		new_user = user_manager.signup(name, email, hash(password))

		if new_user == "already_exists":
			return render_template('signup.html', error="Utilizatorul exista deja!")


		return render_template('signup.html', msg = "Contul dumneavoastră a fost înregistrat!")


	return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)
	loanedbooks = user_manager.getLoanBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, loanedbooks=loanedbooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["Nume"])
	email = str(_form["Email"])
	password = str(_form["Parola"])
	user_manager.update(name, email, hash(password), user_manager.user.uid())

	flash('Informațiile au fost actualizate cu succes!')
	return redirect("/user/")