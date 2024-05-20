from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class AddProductForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    category = StringField("Category", validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[InputRequired()])
