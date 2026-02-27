from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError


app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    age=db.Column(db.Integer, nullable=False)
    filiere = db.Column(db.String(50), nullable=False)

    __table_args__=(
    db.CheckConstraint('age >=18', name='check_age_min_18'),
    )   

    

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students=Student.query.all()
    return render_template('index.html', students=students)



@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        age = int(request.form['age'])
        filiere = request.form['filiere']

        if age < 18:
            error = "❌ L'âge doit être supérieur ou égal à 18 ans."
            return render_template('add_student.html', error=error)

        student = Student(
            nom=nom,
            email=email,
            age=age,
            filiere=filiere
        )

        try:
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('index'))

        except IntegrityError:
            db.session.rollback()
            error = "❌ Email déjà utilisé ou âge invalide."
            return render_template('add_student.html', error=error)

    return render_template('add_student.html')


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))





if __name__=='__main__':
    app.run(debug=True)
