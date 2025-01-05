from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User
from werkzeug.security import check_password_hash

# Inisialisasi Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        # Cek apakah email sudah terdaftar
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'danger')
            return redirect(url_for('routes.register'))

        # Tambahkan pengguna ke database
        new_user = User(username=username, role=role, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('routes.login'))

    return render_template('login.html')


@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'danger')
        return redirect(url_for('routes.login'))
    users = User.get_all_users()
    return render_template('dashboard.html', users=users)


@routes.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))


@routes.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('routes.login'))
    User.delete_user(user_id)
    flash('User deleted successfully.', 'success')
    return redirect(url_for('routes.dashboard'))
