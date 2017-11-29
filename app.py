from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI']='postgres://localhost/students-db'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
modus = Modus(app)

class Student(db.Model):

	__tablename__="students"

	#columns, DDL
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

if __name__ == '__main__':
	app.run(debug=True)	