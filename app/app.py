from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

REQUESTS = Counter('http_request_total',
                   'Total number of requests')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///builds/gitlab-instance-f38b1949/otus_homework_7/app/todo.db'
metrics = PrometheusMetrics(app)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route('/add', methods=["POST"])
def add():
    data = request.form["todo_item"]
    todo = Todo(text=data, complete=False)
    db.session.add(todo)
    db.session.commit()
    # return data # DEBUG REQUEST
    REQUESTS.inc()
    return redirect(url_for("index"))

@app.route('/update', methods=["POST"])
def update():
    # return request.form # DEBUG REQUEST
    REQUESTS.inc()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, threaded=True)
