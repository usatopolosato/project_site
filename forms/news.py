from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


# Форма для добавления/изменения новости Типа 1.
class NewsForm1(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')


# Форма для добавления/изменения новости Типа 2.
class NewsForm2(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    photo = StringField("Ссылка на фото", validators=[DataRequired()])
    submit = SubmitField('Применить')


# Форма для добавления/изменения новости Типа 3.
class NewsForm3(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    video = StringField("Ссылка на видео(поддерживается только YouTube)",
                        validators=[DataRequired()])
    submit = SubmitField('Применить')
