import smtplib, ssl, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

UPLOADS_FOLDER = 'uploads/'

def send_email(contacts_file, sender_email, password, email_subject, email_content, email_client, filters=None):
    # Get contacts
    contacts = []
    with open(UPLOADS_FOLDER+contacts_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            contacts.append(row)

    # Host configuration (Vérifier le serveur de messagerie après le @) (si custom, voir comment faire)
    if email_client == "gmail":
        port = 465
        smtp_server = 'smtp.gmail.com'

    for index, contact in enumerate(contacts):
        if index == 1:
            receiver_email = contact[2]
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
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

def get_fields(contacts_file):
    with open(UPLOADS_FOLDER+contacts_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
    
    return fields

def get_user_params(user_id):
    email = ''
    password = ''
    filepath = 'test.csv'
    email_client = ''
    return [email, password, filepath, email_client]