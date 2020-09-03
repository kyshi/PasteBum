from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Belgelerim/Projects/Flask Projects/PasteBum/notes.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/note/<string:url>", methods=["POST","GET"])
def create_note(url):
    if request.method == "POST":
        url = "add"
        title = request.form.get("title")
        content = request.form.get("content")
        syntax = request.form.get("syntax")
        now = datetime.now()
        url_seed = f"{str(now)}+{title}+{content}"
        newNote = Note(title=title, content=content, syntax=syntax, url=hashlib.sha1(url_seed.encode("utf-8")).hexdigest())
        db.session.add(newNote)
        db.session.commit()
        return redirect(url_for("create_note", url=newNote.url))

    elif url != "add":
        note = Note.query.filter_by(url=url).first()
        line = ""
        for i in range(1, note.content.count("\n")+2):
            line += f"{i}\n"
        return render_template("note.html", title=note.title, content=note.content, syntax=note.syntax, line=line)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    syntax = db.Column(db.String(30))
    url = db.Column(db.String(20))


if __name__ == "__main__":
    app.run(debug=True)