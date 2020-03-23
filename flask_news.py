from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import NewsForm

app = Flask(__name__)
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    news_type = db.Column(db.Enum('推荐', '百家', '本地', '图片'))
    comments = db.relationship('Comments', backref='news',
                                lazy='dynamic')

    def __repr__(self):
        return '<News %r>' % self.title

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000), nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    new_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return '<News %r>' % self.content


@app.route('/')
def index():
    news_list = News.query.filter_by(is_valid=1)
    return render_template("index.html", news_list=news_list)

@app.route('/cat/<name>/')
def cat(name):
    news_list = News.query.filter_by(is_valid=1)
    return render_template("cat.html",name = name, news_list=news_list)

@app.route('/detail/<int:pk>/')
def detail(pk):
    new_obj = News.query.get(pk)
    return render_template("detail.html", new_obj = new_obj)


if __name__ == '__main__':
    app.run(debug=True)