from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.Integer, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method=="POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method=="POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

if __name__ == '__main__':
    app.run()
