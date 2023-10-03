from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'])])


class CaptchaForm(FlaskForm):

    recaptcha = RecaptchaField()
