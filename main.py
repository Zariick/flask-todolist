from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
#Write your own secret key
app.config["SECRET_KEY"] = "YOUR OWN SECRET KEY"
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)

#Initializing the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150), unique=False)
    is_completed = db.Column(db.String(10), unique=False)


with app.app_context():
    db.create_all()

#Creating a form
class TodoForm(FlaskForm):
    todo_point = StringField("Todo Point", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/")
def home():
    todos = db.session.execute(db.select(Todo).order_by(Todo.text)).scalars().all()
    return render_template("home.html", todos=todos)

@app.route("/add", methods=["GET", "POST"])
def add():
    #Doing the action to be able to add some new todos
    form = TodoForm()
    #If form send with no problems and the data was filled
    if form.validate_on_submit():
        new_todo = Todo(
            text=form.todo_point.data,
            is_completed='no'
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form, title="Add todo", h1="Add a new todo to your list")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    #Be able to delete if it's necessary
    #Finding todo_to_delete which we want to delete by id (when we clicked on it)
    todo_to_delete = db.get_or_404(Todo, request.args.get("id"))
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    #Finding current_todo to start editing that
    current_todo = db.get_or_404(Todo, request.args.get('id'))
    form = TodoForm(
        todo_point=current_todo.text
    )
    if form.validate_on_submit():
        #Getting the text to edit it
        current_todo.text = form.todo_point.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", title="Edit todo", h1="Edit current todo", form=form)

@app.route('/complete', methods=["GET", "POST"])
def complete():
    #Doing the action so when press the button complete the current_todo was completed
    current_todo = db.get_or_404(Todo, request.args.get('id'))
    #Changing this attribut to change color of it in the css
    current_todo.is_completed = "yes"
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)