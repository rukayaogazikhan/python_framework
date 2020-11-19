import pysftp
import os
from operator import attrgetter
from paramiko import SSHException, AuthenticationException, PasswordRequiredException
from pysftp.exceptions import CredentialException, ConnectionException, HostKeysException
from datetime import timedelta, datetime, date


class Sftp:
    def __init__(self, host, user, password):
        self.connection = None
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        message = ''

        try:
            self.connection = pysftp.Connection(host=self.host,
                                                username=self.user,
                                                password=self.password,
                                                cnopts=cnopts)
        except ConnectionException:
            message = 'Connection failure for ' + self.host
        except CredentialException:
            message = 'Credential failed for ' + self.host
        except SSHException:
            message = 'SSH failed for ' + self.host
        except AuthenticationException:
            message = 'Authentication failed for ' + self.host
        except PasswordRequiredException:
            message = 'Password required for ' + self.host
        except HostKeysException:
            message = 'Host keys failure for ' + self.host

        return message

    def disconnect(self):
        self.connection.close()

    def get_file(self, remote_path, local_path):

        try:
            self.connection.get(remote_path, local_path)
        except IOError:
            #removing the created empty local file on failure
            os.remove(local_path)
            return 1

        return 0

    def get_files_attributes(self, remote_dir):
        return self.connection.listdir_attr(remotepath=remote_dir)


class SFTPFiles(Sftp):
    def __init__(self, host, user, password, local_folder, remote_path_folder):
        super().__init__(host, user, password)
        self.local_path = local_folder
        self.remote_path = remote_path_folder

    def download_files(self, input_date=datetime.today()):
        input_date = input_date.strftime('%d-%m-%Y')

        self.connect()
        remote_files = self.get_files_attributes(self.remote_path)
        sorted_remote_files = sorted(remote_files, key=attrgetter('st_mtime'), reverse=True)

        for file in sorted_remote_files:
            if datetime.fromtimestamp(file.st_mtime).strftime('%d-%m-%Y') == input_date:
                local_file = self.local_path + file.filename
                remote_file = self.remote_path + file.filename
                self.get_file(remote_file, local_file)
            else:
                pass
        self.disconnect()


if __name__ == '__main__':
    pass