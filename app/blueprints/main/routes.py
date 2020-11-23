from flask import current_app as app, render_template, request, redirect, url_for, session, flash
from flask_login import current_user, login_required
from app import db
from app.blueprints.authentication.models import User

@app.route('/')
@login_required
def index():
    users = sorted(User.query.all(), key=lambda x: x.id)
    context = {
        'user': current_user,
        'users': users,
        'names': [u.display for u in users if u.team == 1],
        'names2': [u.display for u in users if u.team == 2],
        'taken': [u.taken for u in users if u.team == 1],
        'taken2': [u.taken for u in users if u.team == 2]
    }
    return render_template('index.html', **context)

@app.route('/t1')
@login_required
def t1():
    users = sorted(User.query.all(), key=lambda x: x.id)
    context = {
        'user': current_user,
        'users': users,
        'names': [u.display for u in users if u.team == 1],
        'taken': [u.taken for u in users if u.team == 1],
    }
    return render_template('t1.html', **context)

@app.route('/t1btn')
@login_required
def t1btn():
    current_user.team = 1
    db.session.commit()
    return redirect(url_for('t1'))

@app.route('/t2')
@login_required
def t2():
    users = sorted(User.query.all(), key=lambda x: x.id)
    context = {
        'user': current_user,
        'users': users,
        'names2': [u.display for u in users if u.team == 2],
        'taken2': [u.taken for u in users if u.team == 2]
    }
    return render_template('t2.html', **context)

@app.route('/t2btn')
@login_required
def t2btn():
    current_user.team = 2
    db.session.commit()
    return redirect(url_for('t2'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/taken')
def taken():
    current_user.taken += 1
    if current_user.owed > 0:
        current_user.owed -= 1
    db.session.commit()
    if current_user.team == 1:
        return redirect(url_for('t1'))
    else:
        return redirect(url_for('t2'))

@app.route('/giveashot')
def giveashot():
    if current_user.inhand > 0:
        _id = int(request.args.get('id'))
        u = User.query.get(_id)
        u.owed += 1
        current_user.inhand -= 1
        db.session.commit()
        flash(f"You gave {u.display} a shot.", 'success')
    else:
        flash("You don't have a shot to give out. Also, stop inting Jay.", 'primary')
    if current_user.team == 1:
        return redirect(url_for('t1'))
    else:
        return redirect(url_for('t2'))

@app.route('/givepower')
def givepower():
    _id = int(request.args.get('id'))
    u = User.query.get(_id)
    u.inhand = u.inhand + 1
    db.session.commit()
    flash(f"{u.display} can now give out a shot.", 'danger')
    if current_user.team == 1:
        return redirect(url_for('t1'))
    else:
        return redirect(url_for('t2'))