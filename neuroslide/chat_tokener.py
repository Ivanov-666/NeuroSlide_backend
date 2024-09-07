# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import requests


class Tokener:
    def __init__(self, api_key):
        self.token = None
        self.token_end_time = None
        self.api_key = api_key

    def get_access_token(
        self,
    ):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"yandexPassportOauthToken": self.api_key}

        response = requests.request(
            "POST", url, headers=headers, json=data, verify=False
        )
        response_data = response.json()

        self.token = response_data["iamToken"]
        self.token_update_time = datetime.now() + timedelta(hours=1)

    def get_token(
        self,
    ):
        if self.token == None or datetime.now() >= self.token_update_time:
            self.get_access_token()
        return self.token