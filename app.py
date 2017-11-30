from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-students-excuses-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
modus = Modus(app)

class Student(db.Model):
	__tablename__ = "students"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	excuses = db.relationship('Excuse', backref ='student', lazy='dynamic', cascade='all,delete')

	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name 

	def __repr__(self):
		return "The student's name is {} {}.".format(self.first_name, self.last_name)

class Excuse(db.Model):		
	__tablename__="excuses"
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

	def __init__(self,text,student_id):
		self.text = text
		self.student_id = student_id

#RESTful routes for students
@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/students', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		new_student = Student(request.form['first_name'], request.form['last_name'])
		db.session.add(new_student)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('students/index.html', students = Student.query.all())	

@app.route('/students/new')
def new():
	return render_template('students/new.html')

@app.route('/students/<int:id>/edit')
def edit(id):
	return render_template('students/edit.html', student=Student.query.get(id))	

@app.route('/students/<int:id>/show', methods = ['GET', 'POST', 'PATCH','DELETE'])
def show(id):
	found_student = Student.query.get(id)
	if request.method == b'PATCH':
		found_student.first_name = request.form['first_name']
		found_student.last_name = request.form['last_name']
		db.session.add(found_student)
		db.session.commit()
		return redirect(url_for('index'))
	if request.method == b'DELETE':
		db.session.delete(found_student)
		db.session.commit()
		return 	redirect(url_for('index'))
	return render_template('students/show.html', student=found_student)	

# RESTful routing for excuses

@app.route('/students/<int:student_id>/excuses', methods=['GET','POST'])
def excuses_index(student_id):
	if request.method == 'POST':
		new_excuse = Excuse(request.form['text'], student_id)
		db.session.add(new_excuse)
		db.session.commit()
		return redirect(url_for('excuses_index'), student_id = student_id)
	found_student = Student.query.get(student_id)
	return render_template('excuses/index.html', student=found_student)

@app.route('/students/<int:student_id>/excuses/new')
def excuses_new(student_id):
	found_student = Student.query.get(student_id)
	return render_template('excuses/new.html', student=found_student)


@app.route('/students/<int:student_id>/excuses/<int:id>/edit')	
def excuses_edit(student_id, id):
	found_excuse = Excuse.query.get(id)
	return render_template('excuses/edit.html', excuse = found_excuse)

@app.route('/students/<int:student_id>/excuses/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def excuses_show(student_id, id):
	found_excuse = Excuse.query.get(id)
	found_student = Student.query.get(student_id)
	if request.method == b'PATCH':
		found_excuse.text = request.form['text']
		db.session.add(found_excuse)
		db.session.commit()
		return redirect(url_for('excuses_index'), student_id = found_student.id)	

	if request.method == b'DELETE':	
		db.session.delete(found_excuse)
		db.session.commit()
		return redirect(url_for('excuses_index'), student_id = found_student.id)
	return render_template('excuses/show.html', excuse = found_excuse )	
		
if __name__ == '__main__':
	app.run(debug=True)	

