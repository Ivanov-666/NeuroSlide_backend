# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import requests


class Tokener:
    """
    A class to manage the retrieval and storage of access tokens for API authentication.

    Attributes:
        token (str): The current access token.
        token_end_time (datetime): The time when the current token will expire.
        api_key (str): The API key used to request the access token.
    """
    def __init__(self, api_key):
        """
        Initializes the Tokener with the provided API key.

        Args:
            api_key (str): The API key used for authentication with the Yandex Cloud IAM service.
        """
        self.token = None
        self.token_end_time = None
        self.api_key = api_key

    def get_access_token(
        self,
    ):
        """
        Requests a new access token from the Yandex Cloud IAM service.
        """
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
        """
        Retrieves the current access token, refreshing it if necessary.

        Returns:
            str: The current access token.
        """
        if self.token == None or datetime.now() >= self.token_update_time:
            self.get_access_token()
        return self.token