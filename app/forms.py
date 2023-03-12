from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Optional, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[a-zA-Z0-9_]{3,20}$', message='Username must be between 3 and 20 characters and can only contain letters, numbers, and underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    username = StringField('Username', validators=[DataRequired(), Regexp('^[a-zA-Z0-9_]{3,20}$', message='Username must be between 3 and 20 characters and can only contain letters, numbers, and underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class AppletForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Submit')


class DeleteApplet(FlaskForm):
    submit = SubmitField('Delete Applet')
