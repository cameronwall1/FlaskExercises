from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        return render_template("index.html")


    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was an error adding task'
    else:
        # tasks = Todo.query.order_by(Todo.date_created).first()
        return render_template("index.html")

        

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if (request.method == 'POST'):
        pass
    else:
        return render_template("displayvalue.html",task=task)



if __name__ == "__main__":
    app.run(debug=True)