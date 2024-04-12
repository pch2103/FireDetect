from flask import render_template, Response, session, redirect, flash, url_for, request
from app.get_axxon import getAxxonCameraList
from app.get_video import detect_video, get_video, create_model
from app.forms import AxxonServerLoginForm, AxxonServerGetCamerasForm, DataStore
from app import app
import re

data = DataStore()

add = 'http://root:RmskBd9922@DESKTOP-6KKNVN4:8000/camera/list?'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AxxonServerLoginForm()
    result = None
    load = False

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


        session['url'] = ('http://' + form.username.data + ':' + form.password.data + '@' + form.serverip.data + ':'
                          + app.config['NEXT_PORT'])
        result, load = getAxxonCameraList(session['url'] + '/camera/list')

        session['remember_me'] = form.remember_me.data
        flash('data.load {} - {}'.format(load, session['remember_me']))

        if load:
            # Success request
            if form.remember_me.data:
                session['username'] = form.username.data
                session['password'] = form.password.data
                session['serverip'] = form.serverip.data
            else:
                if 'password' in session:
                    session.pop('password')
            session['result'] = result
            return redirect(url_for('virtual_cameras'))
        else:
            if result:
                # Error in request
                if 'password' in session:
                    session.pop('password')
                if 'username' in session:
                    session.pop('username')

    return render_template('index.html', title='Home', form=form, result=result, load=load)


@app.route("/video_feed")
def video_feed():
    if 'camera' in session:
        return Response(detect_video(session['camera']), mimetype='multipart/x-mixed-replace; boundary=frame')
    return redirect(url_for('virtual_cameras'))


@app.route('/virtual_cameras', methods=['GET', 'POST'])
def virtual_cameras():
    result = []
    if 'result' in session:
        result = session['result']
    header = ''
    play_video = False
    form = AxxonServerGetCamerasForm()

    choices = []
    for item in result:
        for key in item:
            choices.append(key)
    form.cameras.choices = choices

    if form.validate_on_submit():
        play_video = False
        vl = None
        for item in result:
            for key in item:
                if key == form.cameras.data:
                    vl = item[key]
                    header = key
                    break

        session['camera'] = (session['url'] + '/live/media/' + re.sub("^hosts/", "", vl))

        play_video = True

    return render_template('virtual_cameras.html', title='Виртуальные камеры',
                           header=header, play_video=play_video, form=form)
