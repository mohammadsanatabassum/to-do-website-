from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.title}"


# ✅ Create DB tables
with app.app_context():
    db.create_all()


# ✅ Home Page (Add + Show)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        complete = request.form.get("complete")

        if title and complete:
            todo = Todo(title=title, complete=complete)
            db.session.add(todo)
            db.session.commit()

        return redirect("/")

    all_todos = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template("index.html", all_todos=all_todos)


# ✅ Delete Todo
@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# ✅ Update Todo
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.complete = request.form.get("complete")
        db.session.commit()
        return redirect("/")

    return render_template("update.html", todo=todo)


if __name__ == "__main__":
    app.run(debug=True)
