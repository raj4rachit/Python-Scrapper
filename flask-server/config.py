from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_PREFERRED_URL_SCHEME'] = 'https'
CORS(app)

app.config['CORS_ALLOW_CREDENTIALS'] = True
app.config['CORS_ORIGIN_ALLOW_ALL'] = True
app.config['CORS_ALLOW_METHODS'] = ['GET', 'POST', 'PUT', 'DELETE']
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_ALL'] = True
app.config['CORS_ALLOW_ALL'] = True
CORS(app)
