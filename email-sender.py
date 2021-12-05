from flask import Flask, render_template, request
from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.simple import FileField
import send_email

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        send_email.send_email(form.file.data, form.email.data, form.password.data, form.subject.data, form.content.data)
    return render_template('index.html', form=form)

if __name__ == "__main__":
   app.run()