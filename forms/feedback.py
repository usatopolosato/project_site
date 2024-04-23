from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


# Форма для обратной связи.
class LetterForm(FlaskForm):
    title = SelectField(u'Вид письма', coerce=int,
                        choices=[(0, 'Предложение'), (1, 'Жалоба')], validate_choice=False)
    content = TextAreaField('Контент письма', validators=[DataRequired()])
    submit = SubmitField('Отправить')
