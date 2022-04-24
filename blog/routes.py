from flask import render_template, url_for, request, redirect, flash
from blog import app, db, models
from blog.models import Comment, User, Post, Rating
from blog.forms import CommentForm, RegistrationForm, LoginForm, RatingForm
from flask_login import login_user, logout_user, current_user
from sqlalchemy import select, func, Table, and_, or_, not_, true
from statistics import mean

@app.route("/")

@app.route("/home")
def home():
  posts=Post.query.all()
  return render_template('home.html', posts=posts)
  
@app.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
  form = CommentForm()
  form2 = RatingForm()
  post = Post.query.get_or_404(post_id)
  comments=Comment.query.all()
  comment=Comment.query.get(post_id)
  ratings=Rating.query.all()
  rating=Rating.query.get(post_id)
  ratingRes= [r.rate for r in db.session.query(Rating.rate).filter_by(post_id=post_id).all()]  #https://stackoverflow.com/a/31842388/17368694
  ratingRes.append(5) # by default all posts start with one 5 star rating
  ratingRes=round(mean(ratingRes), 2)
  exists = bool(db.session.query(Rating).filter(and_(Rating.author_id==current_user.get_id(), Rating.post_id==post_id)).first())
  if request.method == 'POST':
    if request.form['submit'] == 'Comment':
      form.validate_on_submit()
      commented = Comment(text=form.text.data, author_id=current_user.get_id(), post_id=post_id)
      db.session.add(commented)
      flash('Your comment has been posted.')
      db.session.commit()
      return redirect(request.url)
    elif request.form['submit'] == 'Rate' and exists == False:
      form.validate_on_submit()
      rated = Rating(rate=form2.rate.data, author_id=current_user.get_id(), post_id=post_id)
      db.session.add(rated)
      flash('Your rating has been submitted.')
      db.session.commit()
      return redirect(request.url)
    else:
      flash('You have already submitted a rating.')
  return render_template('post.html', title=post.title, post=post, comments=comments, comment=comment, ratings=ratings, rating=rating, form=form, form2=form2, ratingRes=ratingRes)

@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('Registration successful!')
      return redirect(url_for('home'))
  return render_template('register.html',title='Register',form=form)
  

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('You\'ve successfully logged in')
      return redirect(url_for('home'))
    else:
      flash('Invalid username or password.')
  return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return redirect(url_for('home'))

  

