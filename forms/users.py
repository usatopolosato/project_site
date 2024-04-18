from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class ApiForm(FlaskForm):
    apikey = StringField('Активируйте api-key для получения новой роли', validators=[DataRequired()])
    submit = SubmitField('Использовать Api-Key')


class UserForm(FlaskForm):
    submit = SubmitField('Выйти')
