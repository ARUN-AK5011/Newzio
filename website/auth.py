from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
import hashlib

auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('auth.login'))

        password = hashlib.sha256(password.encode()).hexdigest()

        conn = current_app.conn
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        acc = cursor.fetchone()

        if not acc:
            flash('Invalid email or password.', category='error')
            return redirect(url_for('auth.login'))

        session['login_status'] = True
        session['username'] = email
        session['user_id'] = email.split('@')[0]

        return redirect(url_for('news.home'))

    return render_template('components/signin.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('news.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if not email or not name or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('auth.register'))

        password = hashlib.sha256(password.encode()).hexdigest()

        conn = current_app.conn
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )
        acc = cursor.fetchone()

        if acc:
            flash('Email already exists. Please sign in.', category='error')
            return redirect(url_for('auth.login'))

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()

        flash('Account created successfully!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('components/register.html')