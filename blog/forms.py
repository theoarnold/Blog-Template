from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp, Email
from blog.models import User


class RegistrationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(), Regexp('^[\w.-]{3,20}$',message='Your username can only contain letters and numbers and must be under 20 characters.')])
  email = StringField('Email',validators=[DataRequired(), Email()])
  password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm_password', message='Passwords do not match. Try again'), Regexp('^[\w.-]{3,20}$',message='Password is too long or contains invalid characters.')])
  confirm_password = PasswordField('Confirm Password',validators=[DataRequired()])
  submit = SubmitField('Register')
  
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Username already exists. Please choose a different one.')
      
  def validate_email(self, email):
    mail = User.query.filter_by(email=email.data).first()
    if mail is not None:
      raise ValidationError('Email already exists. Please choose a different one.')



class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  submit = SubmitField('Login')


class CommentForm(FlaskForm):
  text = StringField('Comment',validators=[DataRequired()])
  submit1 = SubmitField('Comment')


class RatingForm(FlaskForm):
  rate = StringField('Rating',validators=[DataRequired()])
  submit2 = SubmitField('Rate')



