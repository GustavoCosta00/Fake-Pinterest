# *** ARQUIVO PADRÃO QUE O O FLASK PRECISA ! ***
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "8Lwi2i5JgyKgSNDnFBKMw5YgerXGLB"
app.config["UPLOAD_FOLDER"] = "static/fotos_site"
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from fakePinterest import routes
from fakePinterest import models