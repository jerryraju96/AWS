from html.entities import html5
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    address = db.Column(db.String(100))
    ug = db.Column(db.String(100))
    pg = db.Column(db.String(100))

    def __init__(self, name, email, phone, dob, address, ug, pg):

        self.name = name
        self.email = email
        self.phone = phone
        self.dob = dob
        self.address = address
        self.ug = ug
        self.pg = pg



#This is the index route where we are going to query on all the student data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students = all_data)


#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        ug = request.form['ug']
        pg = request.form['pg']


        my_data = Data(name, email, phone, dob, address, ug, pg)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update student details
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.dob = request.form['dob']
        my_data.address = request.form['address']
        my_data.ug = request.form['ug']
        my_data.pg = request.form['pg']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting student
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Record Has Been Deleted Successfully")

    return redirect(url_for('Index'))



#This route is for retrieving student details
@app.route('/retrieve', methods = ['GET', 'POST'])
def retrieve():

    my_data = Data.query.get(request.form.get('name'))
    search_name = request.form['name']
    if search_name == my_data:
        flash("Student Record/s Found Successfully")
    else:
        flash("No Student Record Found By This Name")
    return redirect(url_for('Index'))












if __name__ == "__main__":
    app.run(debug=True)