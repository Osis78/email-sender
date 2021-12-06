import os

from flask import Flask, request, render_template
from emailsender import send_email, db

from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.simple import FileField

class EmailForm(Form):
    email = StringField('', [
        validators.Length(min=6, max=35),
        validators.DataRequired()
    ])
    name = StringField('', [
        validators.Length(min=3, max=35),
        validators.DataRequired()
    ])
    password = PasswordField('', [validators.DataRequired()])
    file = FileField('')
    subject = StringField('', [
        validators.Length(min=1, max=255),
        validators.DataRequired()
    ])
    content = StringField('', [validators.DataRequired()])

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'email-sender.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return 'Log in'

    @app.route('/emailsender', methods=['GET', 'POST'])
    def email_sender():
        form = EmailForm(request.form)
        if request.method == 'POST' and form.validate():
            send_email.send_email(form.file.data, form.email.data, form.password.data, form.subject.data, form.content.data)
        return render_template('index.html', form=form)

    db.init_app(app)

    return app