from re import match

from flask_wtf import Form

from wtforms import FileField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, ValidationError

from .enums import Realm, Spec

FILE_EXT = r"^[a-zA-Z_]+\.(png|bmp|jpg|jpeg)$"


class LoginForm(Form):
    nick_name = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(Form):
    nick_name = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    retype = PasswordField("Retype", validators=[InputRequired()])

    main_name = StringField("Character", validators=[InputRequired()])
    main_server_str = SelectField("Server", validators=[InputRequired()], choices=Realm.items())
    main_spec_str = SelectField("Spec", validators=[InputRequired()], choices=Spec.items())

    @property
    def main_server(self):
        return Realm(int(self.main_server_str.data))

    @property
    def main_spec(self):
        return Spec(int(self.main_server_str.data))

    def validate(self, extra_validators=None):
        valid = super().validate()
        if self.password.data != self.retype.data:
            self.retype.errors.append("Does not match password")
            return False
        return valid


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
