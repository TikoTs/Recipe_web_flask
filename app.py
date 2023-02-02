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

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    recipe_steps = db.Column(db.String(10000), nullable=False)
    ingredients_numb = db.Column(db.Integer, nullable=False)
    item_src = db.Column(db.String(1000), nullable=False)

    def __str__(self):
        return f'Name: {self.name}; Ingredients: {self.ingredients}; Steps: {self.recipe_steps}'


class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    recipe_steps = db.Column(db.String(10000), nullable=False)
    item_src = db.Column(db.String(1000), nullable=False)

    def __str__(self):
        return f'Name: {self.name}; Ingredients: {self.ingredients}; Steps: {self.recipe_steps}'


app_context = app.app_context()
app_context.push()
db.create_all()

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
   return render_template('food.html', name=current_user.first_name)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        is_digit = 0
        is_upper = 0
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        elif first_name == '' or last_name == '' or password == '':
            flash("Fill in all blanks!")
            return redirect(url_for('signup'))
        elif len(password)<8:
            flash("Password must contain minimum of 8 characters")
            return redirect(url_for('signup'))
        elif len(password)>=8:
            for each in password:
                if each.isdigit():
                    is_digit += 1
                if 65<=ord(each)<=90:
                    is_upper += 1
            if is_digit==0 or is_upper==0:
                flash("Password must contain at least one uppercase character and one number")
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
        is_digit = 0
        is_upper = 0
        if user:
            if len(new_password) < 8:
                flash("Password must contain minimum of 8 characters")
                return redirect(url_for("reset_password"))
            elif len(new_password) >= 8:
                for each in new_password:
                    if each.isdigit():
                        is_digit += 1
                    if each.isupper():
                        is_upper += 1
                if is_digit == 0 or is_upper == 0:
                    flash("Password must contain at least one uppercase character and one number")
                    return redirect(url_for("reset_password"))
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

@app.route('/cocktail_name', methods=['POST', 'GET'])
def cocktail_name():
    if request.method == 'POST':
        name = request.form['cocktail_name'].capitalize()
        cocktail_name = Recipes.query.filter_by(name=name).first()
        if cocktail_name:
            pict_src = cocktail_name.item_src
            cocktail_ingrs = cocktail_name.ingredients.strip('[]')
            cocktail_rcp_steps = cocktail_name.recipe_steps.strip('[]').split(',')
            return render_template('cocktail_name.html', status=cocktail_name, name=name, img=pict_src, ingredients=cocktail_ingrs,steps=cocktail_rcp_steps)
        elif name == '':
            flash('Enter cocktail name')
            return redirect(url_for('cocktail_name'))
        else:
            flash("Cocktails doesn't exist")
            return redirect(url_for('cocktail_name'))
    else:
        return render_template("cocktail_name.html")

@app.route('/meal', methods=['POST', 'GET'])
def meal():
    meals_obj = Meals.query.all()
    if request.method == "POST":
        meal_name = request.form.get("Meals")
        meal_name_db = Meals.query.filter_by(name=meal_name).first()
        if meal_name_db:
            pict_src = meal_name_db.item_src
            meal_ingredients = meal_name_db.ingredients.strip('[]')
            meal_rcp_steps = meal_name_db.recipe_steps.strip('[]').split(',')
            return render_template('meals.html', name=meal_name, img=pict_src,
                                   ingredients=meal_ingredients, steps=meal_rcp_steps, status=meal_name_db)
        else:
            return redirect(url_for('meal'))


    return render_template('meals.html', value_name=meals_obj)

@app.route('/about_us')
def about_us():
    return render_template('aboutUs.html')




if __name__ == "__main__":
    app.run(debug=True)

