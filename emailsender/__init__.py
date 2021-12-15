import os, sys

from flask import Flask, request, render_template, redirect
#from werkzeug.utils import secure_filename
from wtforms import Form, StringField, PasswordField, validators

from emailsender import functions, db

UPLOADS_FOLDER = 'uploads/'

class authForm(Form):
    email = StringField('', [
        validators.Length(min=6, max=50),
        validators.DataRequired()
    ])
    password = PasswordField('', [
        validators.Length(min=8, max=16),
        validators.DataRequired()
    ])

class EmailForm(Form):
    name = StringField('', [
        validators.Length(min=3, max=35),
        validators.DataRequired()
    ])
    subject = StringField('', [
        validators.Length(min=1, max=255),
        validators.DataRequired()
    ])
    filters = StringField('')
    content = StringField('', [validators.DataRequired()])

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'emailsender.sqlite')
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
        form = authForm(request.form)
        if request.method == 'POST' and form.validate():
            return redirect('/emailsender', code=302)
        return render_template('login.html', form=form)
    
    @app.route('/account', methods=['GET', 'POST'])
    def account():
        return 'Compte'

    @app.route('/emailsender', methods=['GET', 'POST'])
    def email_sender():
        user_params = functions.get_user_params(0)
        form = EmailForm(request.form)
        filters = functions.get_fields(UPLOADS_FOLDER+user_params[2])
        editorVars = functions.get_fields(UPLOADS_FOLDER+user_params[2])
        if request.method == 'POST' and form.validate():
            functions.send_email(UPLOADS_FOLDER+user_params[2], user_params[0], user_params[1], form.name.data, form.subject.data, form.content.data, user_params[3], form.filters.data)
        return render_template('emailsender.html', form=form, filters=filters, editorVars=editorVars)

    db.init_app(app)

    return app