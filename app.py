from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ontheedge'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite'
db = SQLAlchemy(app)



app_context = app.app_context()
app_context.push()




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/food')
def food():
   return render_template('food.html')



@app.route('/about_us')
def about_us():
    return render_template('aboutUs.html')




if __name__ == "__main__":
    app.run(debug=True)

