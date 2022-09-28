from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import EmailField, TextAreaField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()] )
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField('Submit')