from flask_wtf import Form

from wtforms import FileField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, ValidationError

from re import match


SERVERS = [
    ("", ""),
    ("arthas", "Arthas"),
    ("blutkessel", "Blutkessel"),
    ("kelthuzad", "Kel'Thuzad"),
    ("veklor", "Vek'lor")
]

FILE_EXT = r"^[a-zA-Z_]+\.(png|bmp|jpg|jpeg)$"


class LoginForm(Form):
    nick_name = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(Form):
    nick_name = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    retype = PasswordField("Retype", validators=[InputRequired()])

    main_name = StringField("Character", validators=[InputRequired()])
    main_server = SelectField("Server", validators=[InputRequired()], choices=SERVERS)


class NewThreadForm(Form):
    title = StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Text", validators=[InputRequired()])


class NewPost(Form):
    text = TextAreaField("New Post", validators=[InputRequired()])


class FileForm(Form):
    file = FileField("New profile picture", validators=[InputRequired()])

    def validate_file(self, _):
        if match(FILE_EXT, self.file.data.filename) is None:
            raise ValidationError()
