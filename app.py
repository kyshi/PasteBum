import hashlib
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/note/<string:url>", methods=["POST", "GET"])
def create_note(url):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        syntax = request.form.get("syntax")
        now = datetime.now()
        url_seed = f"{str(now)}+{title}+{content}"
        newNote = Note(
            title=title,
            content=content,
            syntax=syntax,
            url=hashlib.sha1(url_seed.encode("utf-8")).hexdigest(),
        )
        db.session.add(newNote)
        db.session.commit()
        return redirect(url_for("create_note", url=newNote.url))

    elif request.method == "GET":
        note = Note.query.filter_by(url=url).first()
        line = ""
        for i in range(1, note.content.count("\n") + 2):
            line += f"{i}\n"
        return render_template(
            "note.html",
            title=note.title,
            content=note.content,
            syntax=note.syntax,
            line=line,
        )

@app.route("/api/<string:url>")
def api(url):
    note = url.split("!$")
    title = note[0]
    content = note[1]
    syntax = note[2]
    now = datetime.now()
    url_seed = f"{str(now)}+{title}+{content}"

    newNote = Note(
        title=title,
        content=content,
        syntax=syntax,
        url=hashlib.sha1(url_seed.encode("utf-8")).hexdigest(),
    )
    db.session.add(newNote)
    db.session.commit()
    url_json = [{
        "url": hashlib.sha1(url_seed.encode("utf-8")).hexdigest()
    }]
    return jsonify(url_json)

@app.route("/contributors")
def contributors():
    return render_template("contributors.html")

@app.route("/pastebum")
def pastebum():
    return render_template("pastebum.html")

@app.route("/informative_text")
def informative_text():
    return render_template("informative_text.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    syntax = db.Column(db.String(30))
    url = db.Column(db.String(20))


if __name__ == "__main__":
    db.create_all()
    app.run()