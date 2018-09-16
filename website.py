from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['SECRET_KEY']= '1d2557964bea6d85898400f32419ebcc'
app.config['MONGO_DBNAME'] = 'studentlist'
app.config['MONGO_URI'] ='mongodb://admin:password1@ds257752.mlab.com:57752/studentlist'

mongo=PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.roll.data == int('050') and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/chart')
def chart():
    return render_template('charts.html')  

@app.route('/data')
def data():
    id = request.args.get('id')
    student = mongo.db.charts
    result = student.find_one({'name': id})
    return jsonify({'results' : result['values']})


if __name__ == '__main__':
    app.run(debug=True)