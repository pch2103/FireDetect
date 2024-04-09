from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired


class DataStore():
    url = None
    result = []
    load = False
    loader_on = False
    selected = False
    camera = None

    def reset(self):
        self.result = []
        self.load = False
        self.selected = False
        self.camera = None
        self.loader_on = False

class AxxonServerLoginForm(FlaskForm):
    serverip = StringField('Имя или IP-адрес сервера',
                           validators=[DataRequired()])
    username = StringField('Имя пользователя', render_kw={"placeholder": "Введите имя пользователя"},
                           validators=[DataRequired()])
    password = StringField('Пароль', render_kw={"placeholder": "Введите пароль"}, validators=[DataRequired()],
                            widget=PasswordInput(hide_value=False))
    # password = PasswordField('Пароль', render_kw={"placeholder": "Введите пароль"}, validators=[DataRequired()])
    remember_me = BooleanField('Запомнить параметры для текущей сессии', render_kw={"checked": False})
    login_submit = SubmitField('Подключиться к серверу', render_kw={"onclick": "loadingContent()"})
