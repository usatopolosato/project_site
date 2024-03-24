from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname = StringField('Введите свой псевдоним', validators=[DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Пока нет базы данных"""
    pass
