from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname = StringField('Введите свой псевдоним', validators=[DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    nickname = StringField('Введите свой псевдоним', validators=[DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[DataRequired()])
    surname = StringField('Введите фамилию', validators=[DataRequired()])
    name = StringField('Введите имя', validators=[DataRequired()])
    patronymic = StringField('Введите отчество', validators=[DataRequired()])
    about = StringField('О себе', validators=[DataRequired()])
    avatar = FileField('Фото', validators=[FileRequired(), FileAllowed(['txt'], 'text files only')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')
