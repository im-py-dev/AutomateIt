from flask import Blueprint, render_template, redirect, url_for, request, session, flash, send_file, jsonify, abort
from flask_login import login_user, current_user, login_required, logout_user
from app import login_manager, db, bcrypt
from app.models import User
from app.forms import LoginForm, SignupForm
from sqlalchemy import or_
from flask_jwt_extended import create_access_token


main_bp = Blueprint('main', __name__)


# configure the LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/my-account', methods=['GET', 'POST'])
def my_account():
    login_form = LoginForm()
    signup_form = SignupForm()
    if current_user.is_authenticated:
        uid = current_user.id
        user = User.query.filter_by(id=uid).first()
    else:
        user = None

    context = {
        'user': user,
        'login_form': login_form,
        'signup_form': signup_form
    }
    return render_template('my-account.html', **context)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Get form data
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if request.method == 'POST':
        # Find user by username
        user = User.query.filter_by(username=username).first()
        # if user found
        if user:
            # Check password hash
            if user.check_password(password):
                # Create a JWT access token
                access_token = create_access_token(identity=user.id)
                print(access_token)
                # # Set access_token in session
                # session['access_token'] = access_token
                # Log user in and redirect to homepage
                login_user(user)
                return redirect(url_for('main.index'))
        # If user doesn't exist or password is incorrect, show error message
        flash('Invalid username or password')
        return render_template('login.html', error='Invalid username or password', form=form)
    else:
        # If user is already logged in, redirect to homepage
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        # Not allowed access
        return redirect(url_for('main.index'))


@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    name = form.name.data
    username = form.username.data
    email = form.email.data

    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if user already exists
            user = User.query.filter(or_(User.username == username, User.email == email)).first()
            if user:
                flash('Username/Email already exists')
                return redirect(url_for('main.my_account'))
            # Hash the password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # check users count
            # TODO update this [Bad way, but fast]
            users = User.query.all()
            # Create new user
            new_user = User(
                name=name,
                username=username,
                email=email,
                password=hashed_password,
                is_admin=1 if not users else 0
            )
            db.session.add(new_user)
            db.session.commit()
            # Log in new user and redirect to homepage
            login_user(new_user)
            return redirect(url_for('main.index'))

    else:
        # If user is already logged in, redirect to homepage
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        # Not allowed access
        return redirect(url_for('main.index'))


@main_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
