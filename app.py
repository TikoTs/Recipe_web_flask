from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ontheedge'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite'
db = SQLAlchemy(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


app_context = app.app_context()
app_context.push()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        else:
            session['username'] = username
        login_user(user, remember=True)
        return redirect(url_for('food'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/food')
def food():
   return render_template('food.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        elif first_name == '' or last_name == '' or password == '':
            flash("Fill in all blanks!")
            return redirect(url_for('signup'))

        new_user = User(username=username, first_name=first_name, last_name=last_name,
                        password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        flash("You have successfully signed up")
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            flash('Password Successfully Updated')
            return redirect(url_for('login'))
        elif new_password == '' or username == '':
            flash('Fill in all blanks!')
            return redirect(url_for('reset_password'))
        else:
            flash("Username doesn't exist!")
            return redirect(url_for('reset_password'))
    else:
        return render_template('resetpass.html')

@app.route('/about_us')
def about_us():
    return render_template('aboutUs.html')




if __name__ == "__main__":
    app.run(debug=True)

