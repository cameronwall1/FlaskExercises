from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLACLCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
         return '<Task %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] + " " + request.form['organization']
        # task_content2 = request.form['organization']

        new_task = Todo(content=task_content)
        # new_task2 = Todo(content=task_content2)

        try:
            db.session.add(new_task)
            # db.session.add(new_task2)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an issue adding task"


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting the task'

if __name__ == "__main__" :
    app.run(debug=True)