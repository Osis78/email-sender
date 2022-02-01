import re
import time, datetime

from flask import request, session, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from emailsender.config import app, db, UPLOADS_FOLDER
from emailsender.classes import authForm, EmailForm
from emailsender.models import User, Campaign
from emailsender.functions import get_fields, save_campaign, send_email

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = authForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Informations de connexion invalides. Veuillez réessayer', category='error')
        else:
            session['user_id'] = user.id
            session['email'] = user.email
            session['password'] = password
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('password', None)
    session.pop('current_campaign', None)
    return redirect(url_for('login'))

@app.route('/campagne', methods=['GET', 'POST'])
def campaign():
    if 'user_id' in session:
        filters = get_fields(UPLOADS_FOLDER + 'test.csv')
        editorVars = get_fields(UPLOADS_FOLDER + 'test.csv')
        update_campaign = False
        if request.args.get('c'):
            update_campaign = True
            req_campaign_id = request.args.get('c')
            req_campaign = Campaign.query.filter_by(id=req_campaign_id).first()
            req_name = req_campaign.name
            req_sender = req_campaign.sender
            req_subject = req_campaign.subject
            req_filters = req_campaign.filters
            req_content = req_campaign.content
            if req_campaign.a_envoyer != 1:
                campaign_date = datetime.datetime.fromtimestamp(req_campaign.a_envoyer)
                campaign_date_format = campaign_date.strftime("%d/%m/%Y %H:%M")
                req_aenvoyer = campaign_date_format
            else:
                req_aenvoyer = req_campaign.a_envoyer
            form = EmailForm(name=req_name, sender=req_sender, subject=req_subject, filters=req_filters, content=req_content, a_envoyer=req_aenvoyer)
            # Si id est donné, alors on va préremplir le form + au lieu d'appeler save_campaign on va appeler une fonction update_campaign
        if request.method == 'POST' and form.validate():
            form = EmailForm(request.form)
            campaign_name = form.name.data
            send_date = form.a_envoyer.data
            a_envoyer = int(time.mktime(datetime.datetime.strptime(send_date, "%d/%m/%Y %H:%M").timetuple())) if send_date != "" else 1
            contacts_file = UPLOADS_FOLDER + 'test.csv'
            sender_email = session['email']
            password = session['password']
            sender_name = form.sender.data
            email_subject = form.subject.data
            email_content = form.content.data
            filters = form.filters.data
            contacts_list = send_email(contacts_file, sender_email, password, sender_name, email_subject, email_content, filters, get_only_contacts=True)
            contacts = ','.join(contacts_list)
            if update_campaign == True:
                campaign = save_campaign(campaign_name, sender_name, email_subject, email_content, a_envoyer, filters, contacts, 0, session['user_id'], True, req_campaign_id)
            if update_campaign == False:
                campaign = save_campaign(campaign_name, sender_name, email_subject, email_content, a_envoyer, filters, contacts, 0, session['user_id'])
                db.session.add(campaign)
            db.session.commit()
            session['current_campaign'] = campaign.id
            return redirect(url_for('confirm'))
        return render_template('emailsender.html', form=form, filters=filters, editorVars=editorVars)
    else:
        return redirect(url_for('login'))

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    # Mettre en forme le template + ajouter la fonction d'envoi
    if 'user_id' in session:
        form = EmailForm(request.form)
        campaign_id = session['current_campaign']
        current_campaign = Campaign.query.filter_by(id=campaign_id).first()
        campaign_date = datetime.datetime.fromtimestamp(current_campaign.a_envoyer)
        campaign_date_format = campaign_date.strftime("Le %d/%m/%Y à %H:%M")
        req_aenvoyer = campaign_date_format
        campaign_date = current_campaign.a_envoyer if current_campaign.a_envoyer == 1 else req_aenvoyer
        contacts = current_campaign.contacts.split(",")
        return render_template('confirm.html', form=form, campaign=current_campaign, campaign_date=campaign_date, contacts=contacts)
    else:
        return redirect(url_for('login'))


@app.route('/campagnes')
def campaigns():
    if 'user_id' in session:
        campaigns = Campaign.query.filter_by(user_id=session['user_id']).all()
        for campaign in campaigns:
            if campaign.a_envoyer != 0 and campaign.a_envoyer != 1:
                campaign_date = datetime.datetime.fromtimestamp(campaign.a_envoyer)
                campaign_date_format = campaign_date.strftime("%d/%m/%Y à %H:%M")
                campaign.a_envoyer = campaign_date_format
        return render_template('campaigns.html', campaigns=campaigns)
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()