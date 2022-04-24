from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='post', lazy=True)
    rating = db.relationship('Rating', backref='post', lazy=True)

    
    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password=db.Column(db.String(128))
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)
    rating = db.relationship('Rating', backref='user', lazy=True)

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
        
    @property
    def password(self):
        raise AttributeError('Password is not readable.')
    
    @password.setter
    def password(self,password):
        self.hashed_password=generate_password_hash(password)

        
    def verify_password(self,password):
        return check_password_hash(self.hashed_password,password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.String(2000), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __repr__(self):
        return f"Comment('{self.text}')"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rate = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __repr__(self):
        return f"Rating('{self.rate}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

