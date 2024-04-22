import os
import pathlib

from flask import render_template, Response, session, redirect, flash, url_for, request, abort
from werkzeug.utils import secure_filename

from app.get_axxon import getAxxonCameraList
from app.get_video import detect_video
from app.forms import AxxonServerLoginForm, AxxonServerGetCamerasForm, FileUploadForm, DataStore
from app import app
import re

data = DataStore()


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
        if not form.serverip.data:
            form.serverip.data = app.config['NEXT_SERVER']

    if form.validate_on_submit():

        session['url'] = ('http://' + form.username.data + ':' + form.password.data + '@' + form.serverip.data + ':'
                          + app.config['NEXT_PORT'])
        try:
            result, load = getAxxonCameraList(session['url'] + '/camera/list')
        except Exception as e:
            result = "Server request error"
            load = False

        session['remember_me'] = form.remember_me.data
        # flash('data.load {} - {}'.format(load, session['url']))

        if load:
            # Success request
            session['username'] = form.username.data
            session['password'] = form.password.data
            session['serverip'] = form.serverip.data
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

    return render_template('virtual_cameras.html', title='Виртуальные камеры',
                           header=header, play_video=play_video, form=form)


@app.route('/upload_file')
def file():
    message = ''
    header = ''

    play_video = None

    if 'camera' in session:
        header = os.path.basename(session['camera']).split('/')[-1]

    if 'message' in request.args:
        message = request.args['message']

    if 'play_video' in request.args:
        play_video = request.args['play_video']

    flash('Files3 - {}'.format(session['camera']))

    return render_template('upload_file.html', title='Видео из файла', header=header,
                           message=message, play_video=play_video)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    message = ''
    play_video = False
    uploaded_file = request.files['file']
    upload_folder = os.path.join(os.path.dirname(__file__), 'static/' + app.config['UPLOAD_PATH'])
    filename = secure_filename(uploaded_file.filename)

    flash('Files1 - {}'.format(filename))
    if filename != '':
        try:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return redirect(url_for('file', message='Не верный формат файла'))

            # Upload new file to /upload
            uploaded_file.save(os.path.join(upload_folder, filename))

            session['camera'] = os.path.join(upload_folder, filename)
            play_video = True
        except Exception as e:
            message = 'Ошибки при загрузки файла (' + str(e) + ')'
    else:
        message = 'Не выбран файл'

    flash('Files2 - {}'.format(session['camera']))

    return redirect(url_for('file', message=message, play_video=play_video))
