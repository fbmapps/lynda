from flask import Flask, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

#DATABASE CNFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5433/myapp'
db.init_app(app)
bcrypt = Bcrypt(app)

#Security Protection against CSRF for Flask-WTF to generate Secure Forms
app.secret_key = "development-key"

#ROUTING
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=['GET','POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))  #There is a current Session send the user to Privilege area

	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html",form=form)
		else:
			pw_hash = bcrypt.generate_password_hash(str(form.password.data)).decode('utf-8')
			newuser = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data, pwdhash=pw_hash)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email  #This Create the Basic Session for the user						
			return redirect(url_for('home'))  #HERE WE PROCESS FORM AND TO DB
	

	elif request.method == 'GET':
		return render_template("signup.html",form=form)


@app.route("/login", methods=['GET','POST'])
def login():
	if 'email' in session:
		return redirect(url_for('home'))  #There is a current Session


	form = LoginForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template("login.html",form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and bcrypt.check_password_hash(user.pwdhash,password):
				session['email'] = form.email.data  #This Create the Basic Session for the user						
				return redirect(url_for('home'))  #Privilege Site
			else:
				return redirect(url_for('login'))  #Login Page, because user doesn't exist	
	

	elif request.method == 'GET':
		return render_template("login.html",form=form)


@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

@app.route("/home", methods=['GET','POST'])
def home():
	if 'email' not in session:
		return redirect(url_for('login'))

	
	form = AddressForm()			

	places = []
	my_coordinates=(18.3893976,-65.99671619999998) #My Home Location

	if request.method == 'POST':
		if form.validate == False:
			return render_template("home.html", form=form)
		else:
				
			#Get the Address
			address = form.address.data

			# Query for places around it
			p = Place()
			my_coordinates=p.address_to_latlng(address) #my_coordinates=(18.3893976,-65.99671619999998)
			places = p.query(address)


			# Return the results
			return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


	elif request.method == 'GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)
   	





#MAIN FUNCTIONS
if __name__ == "__main__":
	app.run(debug=True)
