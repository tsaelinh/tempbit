from flask import flash, Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, UserMixin, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.debug = True
app.secret_key="totally secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tempbit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
	return User.query.get(id)

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(32), unique=True)
	password = db.Column(db.String(128))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Go')


@app.route('/feed')
@login_required
def feed():
	return render_template('feed.html')


@app.route('/', methods = ['GET', 'POST'])
@app.route('/signin', methods = ['GET', 'POST'])
def returning_user():
	if current_user.is_authenticated:
		return redirect(url_for('feed'))
	form = LoginForm()
	if form.validate_on_submit():
		if form.username.data is None or form.password.data is None:
			flash("Username or password not given")
			return redirect(url_for('returning_user'))
		user = User.query.filter_by(user=form.username.data).first()
		if user is None or not sha256_crypt.verify(form.password.data, User.query.filter_by(user=form.username.data).first().password):
			flash("Username or password not found")
			return redirect(url_for('returning_user'))
		login_user(user)
		return redirect(url_for('feed'))
	return render_template('signin.html', form=form)

@app.route('/signup', methods = ['GET','POST'])
def new_user():
	if current_user.is_authenticated:
		return redirect(url_for('feed'))
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		if username is None or password is None:
			flash("Incomplete form")
			return redirect(url_for('new_user'))
		if User.query.filter_by(user = username).first() is not None:
			flash("You already exist")
			return redirect(url_for('new_user'))
		hash = sha256_crypt.hash(password)
		add_user = User(user = username, password = hash)
		db.session.add(add_user)
		db.session.commit()
		return redirect(url_for('feed'))
	return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('returning_user'))

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
	app.run()
