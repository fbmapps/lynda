from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

#SIGNUP FORM

class SignupForm(Form):
	first_name = StringField('First Name', validators=[DataRequired('Please enter your First Name')])
	last_name = StringField('Last Name', validators=[DataRequired('Please enter your Last Name')])
	email = StringField('Email', validators=[DataRequired('Please enter your Email'), Email('Please provide a valid email address')])
	password = PasswordField('Password', validators=[DataRequired('Please enter a Password'),Length(min=8,message='Password should be at least 8 characters')])
	submit = SubmitField('Sign Up')


class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired('Please enter your Email'), Email('Please provide a valid email address')])
	password = PasswordField('Password', validators=[DataRequired('Please enter a Password')])
	submit = SubmitField('Sign Up')	


class AddressForm(Form):
	address = StringField('Address', validators=[DataRequired('Please enter an Address')])
	submit = SubmitField('Search')	
