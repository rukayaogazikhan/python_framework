import v1.app.common.functions.oracle as oracle
import v1.app.common.functions.emailer as emailer
import v1.app.config as runtime_configuration
from configparser import ConfigParser
import os


config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), f'../config/{runtime_configuration.runtime_environment}', 'config.ini'))

class Example:
    def __init__(self):
        pass

    @staticmethod
    def run_oracle_query():
        oracle_instance = oracle.OracleQuery(config['database']['database_tns']
                                             , config['database']['database_username']
                                             , config['database']['database_password'])

        parameters = {'OBJECT_TYPES': ['TABLE', 'INDEX', 'CLUSTER']
                      , 'OBJECT_NAME': ['%VIEW%']
                      , 'STARTING_OBJECT_ID': [282]
                      , 'ENDING_OBJECT_ID': [6359]
                      , 'OWNER': ['SYSTEM']
                      }

        results = oracle_instance.run_query("object_queries.sql", parameters)
        return results

    @staticmethod
    def run_send_email():
        email_instance = emailer.EmailNotification(config['email']['email_server']
                                                   , config['email']['email_sender']
                                                   , config['email']['email_username']
                                                   , config['email']['email_password']
                                                   )

        list_of_dictionaries = [{'foo': 12, 'bar': 14},
                  {'moo': 52, 'car': 641},
                  {'doo': 6, 'tar': 84}]

        attachment = os.path.join(os.path.dirname(__file__), '../resources/emails/attachments/test.txt')

        email_parameters = {'SALUTATIONS': "Hello"
                            , 'TABLE': list_of_dictionaries
                            , 'SIGN_OFF': "Me"
                            , 'ATTACHMENT': attachment
                            }

        send_email = email_instance.send_email('html'
                                               , 'Email Table and Attachment'
                                               , "generic_email.html"
                                               , ['testing@test.com']
                                               , email_parameters)
        return send_email
