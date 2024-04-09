from flask import render_template, session, redirect, flash, url_for
from app.get_axxon import getAxxonCameraList
from app.forms import AxxonServerLoginForm, DataStore
from app import app

data = DataStore()

add = 'http://root:RmskBd9922@DESKTOP-6KKNVN4:8000/camera/list?'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AxxonServerLoginForm()

    if 'username' in session and not form.username.data:
        form.username.data = session.get('username')
    if 'password' in session and not form.password.data:
        form.password.data = session.get('password')
    if 'serverip' in session and not form.serverip.data:
        form.serverip.data = session.get('serverip')
    else:
        form.serverip.data = app.config['NEXT_SERVER']

    data.reset()

    if form.validate_on_submit():

        data.url = 'http://' + form.username.data + ':' + form.password.data + '@' + form.serverip.data + ':8000/camera/list'
        data.result, data.load = getAxxonCameraList(data.url)

        session['remember_me'] = form.remember_me.data
        flash('data.load {} - {}'.format(data.load, session['remember_me']))

        if data.load:
            # Success request
            if form.remember_me.data:
                session['username'] = form.username.data
                session['password'] = form.password.data
                session['serverip'] = form.serverip.data
            else:
                if 'password' in session:
                    session.pop('password')
        else:
            if data.result:
                # Error in request
                if 'password' in session:
                    session.pop('password')
                if 'username' in session:
                    session.pop('username')

    return render_template('index.html', title='Home', form=form, result=data.result, load=data.load)


@app.route('/virtual_cameras', methods=['GET', 'POST'])
def virtual_cam():
    form = AxxonServerLoginForm()
    return render_template('virtual_cameras.html', title='Home', form=form)
