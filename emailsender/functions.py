import smtplib, ssl, csv, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itertools import chain, zip_longest

from emailsender.models import Campaign

def save_campaign(campaign_name, sender, subject, content, date_envoi, filters, contacts, is_sent, user_id, update=False, campaign_id=None, confirmed=0):
    if update == False:
        campaign = Campaign(name=campaign_name, sender=sender, subject=subject, content=content, date_envoi=date_envoi, filters=filters, contacts=contacts, confirmed=confirmed, sent=is_sent, user_id=user_id)
    if update == True and campaign_id != None:
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        campaign.name = campaign_name
        campaign.sender = sender
        campaign.subject = subject
        campaign.content = content
        campaign.date_envoi = date_envoi
        campaign.filters = filters
        campaign.contacts = contacts
        campaign.confirmed = confirmed
        campaign.sent = is_sent
    return campaign

def send_email(contacts_file, sender_email, password, sender_name, email_subject, email_content, filters, get_only_contacts=False):
    # Get contacts
    contacts = []
    with open(contacts_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = get_fields(contacts_file)

        if get_only_contacts == False:
            # Get liquid vars
            liquidVars = re.findall('{{(.*?)}}', email_content)
            liquidVarsDict = {}
            for i, field in enumerate(fields):
                if field in liquidVars:
                    liquidVarsDict[field] = i

        if filters:
            filters = str(filters)
            search_terms = re.findall('`(.*?)`', filters)
            operators = re.findall('` (.*?) `', filters)

            query = [x for x in chain(*zip_longest(search_terms, operators)) if x is not None]
            query_without_operators = [x for i, x in enumerate(query) if i % 2 == 0]

            fields_in_query = [x for i, x in enumerate(query_without_operators) if i % 2 == 0]
            fields_position = dict()
            for i, field in enumerate(fields):
                if field in fields_in_query:
                    fields_position[field] = i
            
            for i, arg in enumerate(query):
                if arg in fields_position:
                    query[i] = "row["+str(fields_position[arg])+"].lower()"
                if arg == '!=' or arg == '<' or arg == '>' or arg == '<=' or arg == '>=':
                    query[i+1] = "'"+query[i+1].lower()+"'"
                if arg == "=":
                    query[i] = "=="
                    query[i+1] = "'"+query[i+1].lower()+"'"
                if arg == 'contient':
                    query[i] = 'in'
                    save_query_previous = query[i-1]
                    query[i-1] = '"'+query[i+1].lower()+'"'
                    query[i+1] = save_query_previous.lower()
                if arg == 'ne contient pas':
                    query[i] = 'not in'
                    save_query_previous = query [i-1]
                    query[i-1] = '"'+query[i+1].lower()+'"'
                    query[i+1] = save_query_previous.lower()
                if arg == 'commence par':
                    query[i] = query[i-1]+".startswith("+'"'+query[i+1].lower()+'"'+")"
                    query.remove(query[i+1])
                    query.remove(query[i-1])
                if arg == 'ne commence pas par':
                    query[i] = "not "+query[i-1]+".startswith("+'"'+query[i+1].lower()+'"'+")"
                    query.remove(query[i+1])
                    query.remove(query[i-1])
                if arg == 'se termine par':
                    query[i] = query[i-1]+".endswith("+'"'+query[i+1].lower()+'"'+")"
                    query.remove(query[i+1])
                    query.remove(query[i-1])
                if arg == 'ne se termine pas par':
                    query[i] = "not "+query[i-1]+".endswith("+'"'+query[i+1].lower()+'"'+")"
                    query.remove(query[i+1])
                    query.remove(query[i-1])
                if arg == 'et':
                    query[i] = 'and'
                if arg == 'ou':
                    query[i] = 'or'
            
            final_query = ' '.join(query)
            for i, row in enumerate(csvreader):
                if i > 0:
                    exec('if '+final_query+': contacts.append(row)')
                    
        else:
            for i, row in enumerate(csvreader):
                if i > 0:
                    contacts.append(row)

    if get_only_contacts == True:
        display_contacts = []
        for contact in contacts:
            display_contacts.append(contact[2])
        return display_contacts

    # Host configuration
    port = 465
    smtp_server = 'authsmtp.securemail.pro'

    for row in contacts:
        #Insert liquid vars instead of field names
        new_email_content = email_content
        if liquidVars:
            for liquidVar in liquidVarsDict:
                new_email_content = new_email_content.replace("{{" + liquidVar + "}}", row[liquidVarsDict[liquidVar]])
                    
        receiver_email = row[2] # En fonction du fichier
        message = MIMEMultipart("alternative")
        message['Subject'] = email_subject
        message['From'] = sender_name + ' <' + sender_email + '>'
        message['To'] = receiver_email
        #text = ''
        html = new_email_content
        #part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        #message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

def get_fields(contacts_file):
    with open(contacts_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
    
    return fields