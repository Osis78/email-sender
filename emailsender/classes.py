from wtforms import Form, StringField, PasswordField, validators

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
        validators.Length(min=3, max=70),
        validators.DataRequired()
    ])
    sender = StringField('', [
        validators.Length(min=3, max=35),
        validators.DataRequired()
    ])
    subject = StringField('', [
        validators.Length(min=1, max=255),
        validators.DataRequired()
    ])
    filters = StringField('')
    content = StringField('', [validators.DataRequired()])
    date_envoi = StringField('', [
        validators.Length(min=0, max=16)
    ])