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

	#instantiate class information in rows
	def __init__(self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name
	
	#making things readable	
	def __repr__(self):
		return "The student's name is {} {}.".format(self.first_name, self.last_name)
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
	return render_template('index.html', students=Student.query.all())

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
	
	return render_template('show.html', student = found_student)

	
@app.route('/student/<int:student_id>/edit')
def edit(student_id):
	found_student = Student.query.get_or_404(student_id)
	return render_template('edit.html', student = found_student)

if __name__ == '__main__':
	app.run(debug=True)	