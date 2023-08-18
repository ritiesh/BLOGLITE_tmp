import os
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_restful import Resource, Api
from applications.database import db
from flask_uploads import UploadSet, IMAGES, configure_uploads
from applications.config import *
from applications.models import *


app = None
api = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api


app, api = create_app()

UPLOAD_FOLDER = os.path.join('static','photos')
# print(UPLOAD_FOLDER)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'secretiveness404'
# app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from applications.controllers import *

from applications.api import *

if __name__ == '__main__':
    app.run(debug=True)
