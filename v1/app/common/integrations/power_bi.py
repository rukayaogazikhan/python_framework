import requests
import v1.app.common.logs as logging

HTTP_OK_CODE = 200


class PowerBI:
    def __init__(self):
        self.workspaces = None
        self.url = "https://api.powerbi.com/v1.0/myorg/"
        self.access_token = self.api_login()
        self.headers = {
                            "Authorization": "Bearer " + self.access_token,
                            "Content-Type": "application/json",
                            "If-Match": '*'
                        }

    def api_login(self):
        data = {
            'grant_type': self.grant_type,
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': 'https://analysis.windows.net/powerbi/api'
        }

        response = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
        return response.json().get('access_token')

    def get_workspaces(self):
        access_token = self.api_login()
        url = self.url + "groups"
        response = requests.get(url, headers=self.headers)

        if response.status_code == HTTP_OK_CODE:
            self.workspaces = response.json()["value"]
            return self.workspaces
        else:
            logging.logger.error("Failed to fetch workspaces!")
            self.raise_http_error(response)

    @staticmethod
    def get_workspace_objects():
        return ['users', 'dataflows', 'datasets', 'reports', 'dashboards']

    def get_object_in_workspace(self, workspace_name, object_type):
        workspace_id = self.find_id_by_name("workspace", self.workspaces, workspace_name)
        report_url = self.url + f"groups/{workspace_id}/{object_type}"

        response = requests.get(report_url, headers=self.headers)
        if response.status_code == HTTP_OK_CODE:
            return response.json()["value"]
        else:
            logging.logger.error(f"Error getting {object_type} from workspace")

    def get_datasets_in_dataflow(self, workspace_name):
        workspace_id = self.find_id_by_name("workspace", self.workspaces, workspace_name)
        datasets_dataflow_link_url = self.url + f"groups/{workspace_id}/datasets/upstreamDataflows"

        response = requests.get(datasets_dataflow_link_url, headers=self.headers)
        if response.status_code == HTTP_OK_CODE:
            return response.json()["value"]
        else:
            logging.logger.error("Error getting datasets from workspace")

    def find_object_by_id(self, object_type, id):
        pass

    @staticmethod
    def find_id_by_name(product, name):
        for item in product:
            if item["name"] == name:
                return item["id"]

    @staticmethod
    def raise_http_error(response):
        blah = f"Expected response code(s) {HTTP_OK_CODE}, got {response.status_code}: {response.text}"
        logging.logger.error(blah)
        return blah