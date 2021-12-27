from os import replace
import smtplib, ssl, csv, re, unicodedata, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itertools import chain, zip_longest

uploads_folder = '../uploads/'

contacts_file = uploads_folder+''
sender_email = ''
password = ''
sender_name = ''
email_subject = ''
email_content = ''
email_client = ''
filters = ''

def get_fields(contacts_file):
    with open(contacts_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
    
    return fields

def send_email(contacts_file, sender_email, password, sender_name, email_subject, email_content, email_client, filters):

    # Get contacts
    contacts = []
    with open(contacts_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = get_fields(contacts_file)

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

    # Host configuration (Vérifier le serveur de messagerie après le @) (si custom, voir comment faire)
    if email_client == "gmail":
        port = 465
        smtp_server = 'smtp.gmail.com'
    else:
        port = 465
        smtp_server = 'smtp.gmail.com'

    for index, contact in enumerate(contacts):
        #Insert liquid vars instead of field names
        if liquidVars:
            for liquidVar in liquidVarsDict:
                email_content = email_content.replace("{{" + liquidVar + "}}", contact[liquidVarsDict[liquidVar]])
        receiver_email = contact[2] # En fonction du fichier
        message = MIMEMultipart("alternative")
        message['Subject'] = email_subject
        message['From'] = sender_email
        message['To'] = receiver_email
        #text = ''
        html = email_content
        #part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        #message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        #with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #    server.login(sender_email, password)
        #    server.sendmail(sender_email, receiver_email, message.as_string())

send_email(contacts_file, sender_email, password, sender_name, email_subject, email_content, email_client, filters)