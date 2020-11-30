from hashlib import blake2b
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
        line = ""
        for i in range(1, content.count("\n") + 2):
            line += f"{i}\n"
        newNote = Note(
            title=title,
            content=content,
            syntax=syntax,
            date=now,
            data_size=len(content.replace("\n", ""))+len(title)+1-int(line[-2]),
            line=line,
            url=blake2b(url_seed.encode("utf-8"), digest_size=5).hexdigest(),
        )
        db.session.add(newNote)
        db.session.commit()
        return redirect(url_for("create_note", url=newNote.url))

    elif request.method == "GET":
        note = Note.query.filter_by(url=url).first()
        return render_template(
            "note.html",
            title=note.title,
            content=note.content,
            syntax=note.syntax,
            date=note.date[:19],
            data_size=note.data_size,
            line=note.line,
        )

@app.route("/api/create_note/<string:title>/<string:content>/<string:syntax>")
def api_crete_note(title, content, syntax):
    title = title
    content = content
    syntax = syntax
    now = datetime.now()
    url_seed = f"{str(now)}+{title}+{content}"
    line = ""
    for i in range(1, content.count("\n") + 2):
        line += f"{i}\n"

    newNote = Note(
        title=title,
        content=content,
        syntax=syntax,
        date=now,
        data_size=len(content)+len(title),
        line=line,
        url=blake2b(url_seed.encode("utf-8"), digest_size=5).hexdigest(),
    )
    db.session.add(newNote)
    db.session.commit()
    json_data = [{
        "url": blake2b(url_seed.encode("utf-8"), digest_size=5).hexdigest()
    }]
    return jsonify(json_data)

@app.route("/api/view_note/<string:url>")
def api_view_note(url):
    note = Note.query.filter_by(url=url).first()
    title = note.title,
    content = note.content,
    syntax = note.syntax,
    date = note.date[:19],
    data_size = note.data_size,
    line = note.line,
    json_data = [{
        "url": url,
        "title": title[0],
        "content": content[0],
        "syntax": syntax[0],
        "details":[
            {
                "date": date[0],
                "data_size": data_size[0],
                "line": line[0]
            }
        ]
    }]
    return jsonify(json_data)

@app.route("/api/documentation")
def api_doc():
    return render_template("api_doc.html")

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
    date = db.Column(db.String(30)) 
    data_size = db.Column(db.Integer)
    line=db.Column(db.Text)
    url = db.Column(db.String(20))


if __name__ == "__main__":  
    db.create_all()
    app.run()