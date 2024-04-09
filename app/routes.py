from flask import render_template, redirect, flash, url_for
import socket
from app.get_axxon import getAxxonCameraList
from app.forms import AxxonServerLoginForm, DataStore
from app import app

data = DataStore()

add = 'http://root:RmskBd9922@DESKTOP-6KKNVN4:8000/camera/list?'
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AxxonServerLoginForm()
    form.serverip.data = socket.gethostname()

    if form.validate_on_submit():
        data.url = 'http://' + form.username.data + ':' + form.password.data + '@' + form.serverip.data + ':8000/camera/list'
        data.result, data.load = getAxxonCameraList(data.url)
        flash('Data {}'.format(data.result))


    return render_template('index.html', title='Home', form=form)

@app.route('/virtual_cameras', methods=['GET', 'POST'])
def virtual_cam():
    form = AxxonServerLoginForm()
    return render_template('virtual_cameras.html', title='Home', form=form)
