#!/usr/bin/env python3.6
import smtplib
import v1.app.common.functions.files as file_processor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tabulate import tabulate
import re
import os

#TO DO
# Looping through attachement names

class EmailNotification:
    def __init__(self, server, sender, username, password):
        self.server = server
        self.sender = sender
        self.username = username
        self.password = password

    @staticmethod
    def validate_email_addresses(email_address):
        email_regex = "([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"

        if re.match(email_regex, email_address, re.IGNORECASE):
            is_valid = True
        else:
            is_valid = False

        return is_valid

    @staticmethod
    def find_email_template(template_name):
        template_files = file_processor.Files(os.path.join(os.path.dirname(__file__),
                                                           '../../resources/emails/templates'))
        path_to_query = template_files.search_folders(name=template_name)[0]
        email_template = template_files.read_file_to_string(path_to_query)

        return email_template

    @staticmethod
    def tabulate_results(list_of_results):
        if list_of_results is None or len(list_of_results) == 0:
            pass
        else:
            header = list_of_results[0].keys()
            rows = [x.values() for x in list_of_results]
            table_of_results = tabulate(rows, header, tablefmt="html")
            return table_of_results

    def check_mail_sent(self):
        pass
        # https://docs.microsoft.com/en-us/graph/api/mailfolder-get?view=graph-rest-1.0&tabs=http
        # stop duplicate mails going out

    def build_email(self, template_name, email_parameters):
        template = self.find_email_template(template_name)
        attachments = []

        for key, email_parameter in email_parameters.items():
            if isinstance(email_parameter, list):
                for i in email_parameter:
                    if os.path.isfile(str(i)):
                        email_parameters[key] = os.path.basename(", ".join(email_parameter))
                        attachments.append(i)
                    # if list of dictionaries convert to a html table
                    elif isinstance(i, dict):
                        email_parameters[key] = self.tabulate_results(email_parameter)
                    elif isinstance(i, str):
                        email_parameters[key] = ", ".join(email_parameter)
            elif os.path.isfile(email_parameter):
                    email_parameters[key] = os.path.basename(email_parameter)
                    attachments.append(email_parameter)

        email_body = template.format(**email_parameters)

        return email_body, attachments

    def send_email(self, format, subject, template_name, to, email_parameters):
        return_message = None

        # validate emails
        try:
            to = [i for i in to if self.validate_email_addresses(i)]
        except smtplib.SMTPHeloError:
            return_message.append(f'Invalid Emails: {[i for i in to if not self.validate_email_addresses(i)]}')

        # get email body and attachments
        email_body, attachments = self.build_email(template_name, email_parameters)

        # set email type
        message = MIMEMultipart("alternative", None, [MIMEText(email_body, format)])

        # set email attachments
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = ", ".join(to)

        for f in attachments or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            message.attach(part)

        # send email
        try:
            server = smtplib.SMTP(self.server)
        except (smtplib.SMTPConnectError,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPException,
                smtplib.SMTPResponseException
                ):
            return_message = 'Email Failed: ' + 'SMTP server connection not established!'

        try:
            server.ehlo()
        except smtplib.SMTPHeloError:
            server.quit()
            return_message = 'Email Failed: ' + 'SMTP server refused our HELO message!'

        try:
            server.starttls()
        except smtplib.SMTPHeloError:
            return_message = 'Email Failed: ' + 'SMTP server connection not in TLS mode!'

        try:
            server.login(self.sender, self.password)
        except (smtplib.SMTPHeloError,
                smtplib.SMTPAuthenticationError,
                smtplib.SMTPNotSupportedError,
                smtplib.SMTPException):
            return_message = 'Email Failed: ' + 'Email Login Unsuccessful!'

        try:
            rejected_recipients = server.sendmail(self.sender, to, message.as_string())
            if len(rejected_recipients) <= 0:
                return_message = 'Emailed Successfully'
            if len(rejected_recipients) > 0:
                return_message = 'Email Failed to Send'
                # log email failed str(rejected_recipients)
        except (smtplib.SMTPHeloError,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPDataError,
                smtplib.SMTPNotSupportedError) as e:
            return_message = 'Email Failed to Send'
            # log error str(e)

        server.quit()

        return return_message


if __name__ == '__main__':
    pass