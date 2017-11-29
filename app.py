from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://localhost/students-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
modus = Modus(app)

class Student(db.Model):

	__tablename__="students"

	#columns, DDLs
	student_id = db.Column(db.Integer, primary_key =True)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	excuses = db.relationship('Excuse', backref = 'student', lazy = 'dynamic', cascade = 'all,delete')

	#instantiate class information in rows
	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name
	
	#making things readable	
	def __repr__(self):
		return "The student's name is {} {}.".format(self.first_name, self.last_name)

class Excuse(db.Model):

	__tablename__="excuses"		

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	is_believable = (db.Boolean)
	student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))

	def __init__(self, name, is_believable, student_id):
		self.name = name
		self.is_believable = is_believable
		self.student_id = student_id

#route			
@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/student', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		new_student = Student(
			request.form['first_name'], 
			request.form['last_name']
			)
		db.session.add(new_student)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('students/index.html', students=Student.query.all())

@app.route('/student/new')
def new():
	return render_template('new.html')

@app.route('/student/<int:student_id>', methods=['GET', 'DELETE', 'PATCH'])
def show(student_id):
	found_student = Student.query.get_or_404(student_id)
	if request.method == b'PATCH':
		found_student.first_name = request.form['first_name']
		found_student.last_name = request.form['last_name']
		db.session.add(found_student)
		db.session.commit()
		return redirect(url_for('index'))
	if request.method == b'DELETE':
		db.session.delete(found_student)
		db.session.commit()
		return redirect(url_for('index'))
	
	return render_template('students/show.html', student = found_student)

@app.route('/student/<int:student_id>/edit')
def edit(student_id):
	found_student = Student.query.get_or_404(student_id)
	return render_template('students/edit.html', student = found_student)

# excueses route
@app.route('/student/<int:student_id>/excuses/', methods=['GET', 'POST'])
def excuses_index(student_id):
	#if we make a post request
	if request.method == 'POST':
		# create an instance 
		new_excuse = Excuse(request.form['name'], student_id)
		db.session.add(new_excuse)
		db.session.commit()
		return redirect(url_for('excuses_index', student_id=student_id))
	student = Student.query.get(student_id)
	return render_template('excuses/index.html', student = student)

@app.route('/student/<int:student_id>/excuses/new')
def excuses_new(student_id):
	student = Student.query.get(student_id)
	return render_template('excuses/new.html', student = student)

@app.route('/student/<int:student_id>/excuses/<int:id>', methods= ['PATCH', 'DELETE', 'GET', 'POST'])		
def excuses_show(student_id, id):
	excuse = Excuse.query.get(id)
	if request.method == b"PATCH":
		excuse.test = request.form['name']
		db.session.add(excuse)
		db.session.commit()
		return redirect(url_for('index'))
	if request.method == b"DELETE": 
		db.session.delete(excuse)
		db.session.commit()	
		return redirect(url_for('index'), student_id=student_id)
	return render_template('excuses/show.html', excuse = excuse)	

@app.route('/student/<int:student_id>/excuses/<int:id>/edit')
def excuses_edit(student_id, id):
	excuse = Excuse.query.get(id)
	return render_template('excuses/edit.html', excuse=excuse)

if __name__ == '__main__':
	app.run(debug=True)	