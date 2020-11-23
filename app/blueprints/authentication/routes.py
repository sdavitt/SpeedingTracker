from app import db
from flask import request, render_template, flash, redirect, url_for
from .import bp as authentication
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .forms import ProfileForm, InfoForm

@authentication.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        r = request.form
        if r.get('confirm_password') == r.get('password'):
            data = {
                'username': r.get('username'),
                'display': r.get('display'),
                'password': r.get('password'),
            }
            u = User(username=data['username'], display=data['display'], password=data['password'])
            u.hash_password(u.password)
            db.session.add(u)
            db.session.commit()
            flash("You have registered successfully", 'primary')
            return redirect(url_for('authentication.login'))
    return render_template('register.html')

@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = request.form
        user = User.query.filter_by(username=r.get('username')).first()
        if user is None or not user.check_password(r.get('password')):
            flash("You have used either an incorrect username or password", 'danger')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=r.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash("You have logged in successfully", 'success')
        return redirect(next_page)
    return render_template('login.html')

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'info')
    return redirect(url_for('authentication.login'))

@authentication.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = {
        'id': current_user.id,
        'username': current_user.username,
        'display': current_user.display,
        'team': current_user.team,
    }
    form = InfoForm()
    form.team.data = user['team']
    form.display.data = user['display']

    if form.validate_on_submit():
        u = User.query.get(user['id'])
        
        u.team = request.form.get('team')
        u.display = request.form.get('display')

        db.session.commit()
        flash('Your information has been updated successfully', 'info')
        return redirect(url_for('authentication.profile'))
    context = {
        'user': user,
        'form': form
    }
    return render_template('profile.html', **context)

@authentication.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    current_user.inhand = 0
    current_user.owed = 0
    current_user.taken = 0
    db.session.commit()
    flash('Your counts have been reset.', 'info')
    return redirect(url_for('authentication.profile'))


@authentication.route('/resetnotshots', methods=['GET', 'POST'])
@login_required
def resetnotshots():
    current_user.inhand = 0
    current_user.owed = 0
    db.session.commit()
    flash('Your counts have been reset.', 'info')
    return redirect(url_for('authentication.profile'))

@authentication.route('/removeashot', methods=['GET', 'POST'])
@login_required
def removeashot():
    current_user.taken += -1
    db.session.commit()
    flash('You removed a shot... bitch move.', 'info')
    return redirect(url_for('authentication.profile'))