from flask import Flask, render_template, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    desc = db.Column(db.String(120), unique=False, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)


@app.route("/add", methods=["GET", "POST"])
def add():
    lis = []
    data = request.get_json()
    title = data['title']
    desc = data['desc']
    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                   "pub_date": todo.pub_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def updateTodo(id):
    lis = []
    data = request.get_json()
    title = data['title']
    desc = data['desc']
    print(title, desc)
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                   "pub_date": todo.pub_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@app.route("/delete/<int:id>/", methods=["GET", "POST"])
def deleteTodo(id):
    lis = []
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                   "pub_date": todo.pub_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@app.route("/show", methods=["GET", "POST"])
def show():
    lis = []
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                   "pub_date": todo.pub_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
