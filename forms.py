from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])
    lbs_or_kg = StringField('lbs or kg',
                          validators=[DataRequired(),])

    weight = IntegerField('Weight',
                          validators=[DataRequired()]
                          )

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


    submit = SubmitField('Sign up')




class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember me')
        submit = SubmitField('Login')

class CalculatorForm(FlaskForm):
        lbs_or_kg = StringField('lbs_or_kg',validators=[DataRequired(), Length(min=2, max=3)])
        weight = IntegerField('weight',validators=[DataRequired()])
        minutes_of_exercise = IntegerField('minutesOfExercise',validators=[DataRequired()])
        submit = SubmitField('Calculate')
