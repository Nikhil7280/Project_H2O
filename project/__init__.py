from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_manager,LoginManager
import stripe
app=Flask(__name__)
public_key='pk_test_51JqEebSEhjJ0OK35gH2wXCL17vaigmFloJ1dyEgpsYwLrwvqGT0PLlL3Fl7PASrPeXdfUkbZGTzyLc9h6qeacjyV00iyWEoBPG'
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"
# #######DATABASE SETUP######
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']="MYSECRETKEY"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)
# #############################################

login_manager=LoginManager()

login_manager.init_app(app)
login_manager.login_view='users.login'

from project.core.views import  core
from project.users.views import users
from project.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
