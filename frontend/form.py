from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired
from frontend import app

pictures = UploadSet('photos', IMAGES)
configure_uploads(app, pictures)

class UploadForm(FlaskForm):
    pictures = FileField(
        "Picture",
        validators=[
            FileAllowed(pictures, "Only pictures are allowed"),
            FileRequired("File should not be empty")
        ]
    )
    key = StringField(
        "Key",
        validators=[ 
            DataRequired()
        ]
    )
    submit = SubmitField("Upload")