import requests
import os
import cgi
import requests
import shutil
import mimetypes
import re


# share point logic
class Sharepoint:
    def __init__(self, username, password, client_id, client_secret):
        self.grant_type = 'password'
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    # SHAREPOINT LOGIN
    def login(self):
        data = {
            'grant_type': self.grant_type,
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': 'https://graph.microsoft.com',
        }

        response = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
        return response.json().get('access_token')

    def list_folder_items(self, site_id, folder_id):
        access_token = self.login()
        header = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "If-Match": '*'
        }

        folder_items = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/children",
            headers=header).json().get('value')

        return folder_items

    def search_for_file(self, site_id, folder_id, item_name):
        folder_items = self.list_folder_items(site_id, folder_id)
        for i in folder_items:
            if re.match(i['name'], item_name, re.IGNORECASE):
                file_id = i['id']

        return file_id

    def download_file(self, site_id, drive_id, folder_id, local_file_directory, remote_file_name):
        access_token = self.login()
        header = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "If-Match": '*'
        }

        documents = self.list_folder_items(site_id, folder_id)

        # Download document matching specified file name
        for document in documents:
            if document['name'] == remote_file_name:
                item_id = document['id']

                response = requests.get(
                    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content",
                    stream=True, headers=header)

                #print(response.status_code)

                if response.status_code != 200:
                    raise ValueError('Failed to download')

                params = cgi.parse_header(
                    response.headers.get('Content-Disposition', ''))[-1]
                if 'filename' not in params:
                    raise ValueError('Could not find a filename')

                filename = os.path.basename(params['filename'])
                abs_path = os.path.join(local_file_directory, filename)
                with open(abs_path, 'wb') as target:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, target)

                return filename

    def replace_existing_file(self, site_id, drive_id, folder_id, local_file_path, local_file_name):
        access_token = self.login()
        header = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        file_path = os.path.join(local_file_path, local_file_name)

        documents = self.list_folder_items(site_id, folder_id)

        # Upload document matching specified file name
        for document in documents:
            if document['name'] == local_file_name:
                item_id = document['id']

                response = requests.put(
                    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/content"
                    , stream=True, headers=header, data=open(file_path, 'rb'))
                #print(response.status_code)
                #print(response.text)

    def upload_new_file(self, drive_id, parent_id, local_file_path, local_file_name):
        access_token = self.login()
        header = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        file_path = os.path.join(local_file_path, local_file_name)

        response = requests.put(
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_id}:/{local_file_name}:/content"
            , stream=True, headers=header, data=open(file_path, 'rb'))

        #print(response.status_code)
        #print(response.text)


if __name__ == '__main__':
    pass

