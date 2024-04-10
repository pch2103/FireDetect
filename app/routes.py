from time import sleep

from flask import render_template, Response, session, redirect, flash, url_for, request
from app.get_axxon import getAxxonCameraList
from app.get_video import detect_video
from app.forms import AxxonServerLoginForm, AxxonServerGetCamerasForm, DataStore
from app import app
import re

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

        data.url = ('http://' + form.username.data + ':' + form.password.data + '@' + form.serverip.data + ':'
                    + app.config['NEXT_PORT'])
        data.result, data.load = getAxxonCameraList(data.url + '/camera/list')

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
            session['result'] = data.result
            return redirect(url_for('virtual_cameras'))
        else:
            if data.result:
                # Error in request
                if 'password' in session:
                    session.pop('password')
                if 'username' in session:
                    session.pop('username')

    return render_template('index.html', title='Home', form=form, result=data.result, load=data.load)

@app.route("/video_feed")
def video_feed():
    res = detect_video(data.camera)
    return Response(res, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/virtual_cameras', methods=['GET', 'POST'])
def virtual_cameras():
    result = session.get('result')
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
        for item in data.result:
            for key in item:
                if key == form.cameras.data:
                    vl = item[key]
                    header = key
                    break

        data.camera = (data.url + '/live/media/' + re.sub("^hosts/", "", vl))

        play_video = True

    return render_template('virtual_cameras.html', title='Виртуальные камеры',
                           play_video=play_video, plamessage=data.camera, form=form)
