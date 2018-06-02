from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)

## Config MySQL
app.config['MYSQL_HOST']   	    = 'localhost'
app.config['MYSQL_USER']	    = 'root'
app.config['MYSQL_PASSWORD']    = 'root'
app.config['MYSQL_DB'] 	        = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

## init MYSQL
mysql = MySQL(app)

## Redirecting and renter html page
@app.route('/')
def home():
	return render_template('index.html')	

@app.route('/about')
def about():
	return render_template('about.html')	

@app.route('/articles')
def articals():
	return render_template('articles.html', articles = Articles())	

@app.route('/article/<string:id>')
def artical(id):
	return render_template('article.html', id=id)


class RegistorForm(Form):
	name 		= StringField('Name',[validators.Length(min=1, max=50)])
	username    = StringField('Username',[validators.Length(min=4,max=25)])
	email       = StringField('Email',[validators.Length(min=5,max=50)])
	password    = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message= 'password do not match'),
		validators.Length(min=5,max=50)
		])
	confirm     = PasswordField('Confirm Password')



@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistorForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

#open mysql connction
		cur = mysql.connection.cursor()
#Use mysql query 
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
#mysql commit to db
		mysql.connection.commit()
#mysql close connection
		cur.close()
#Sucess message
		flash('You are now registered and can log in', 'success')
		return redirect(url_for('login'))

	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']

		cur = mysql.connection.cursor()
		result  =cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
			data = cur.fetchone()
			password = data['password']
			
			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid login'
				return render_template('login.html', error=error)
			cur.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)


	return render_template('login.html')



def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap



@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
	return render_template('dashboard.html')

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))



if __name__ =='__main__':
	app.secret_key='mano42302@'
	app.run(debug =True)