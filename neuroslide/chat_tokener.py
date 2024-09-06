import datetime
import uuid
import requests

class Tokener:
    def __init__(self, api_key):
        self.token = None
        self.token_end_time = None
        self.api_key = api_key

    def get_access_token(self,):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = 'scope=GIGACHAT_API_CORP'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Basic {self.api_key}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response_data = response.json()

        self.token = response_data['access_token']
        self.token_end_time = datetime.datetime.fromtimestamp(response.json()["expires_at"]/1000)

    def get_token(self,):
        if self.token == None or datetime.datetime.now() >= self.token_end_time:
            self.get_access_token()
        return self.token
