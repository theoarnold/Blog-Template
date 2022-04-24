from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '552ba926b6303eb3593c9a63fdbd1e90ced12f47111c9786'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1847553:Blogdatabase456@csmysql.cs.cf.ac.uk:3306/c1847553_blog'
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)


from blog import routes