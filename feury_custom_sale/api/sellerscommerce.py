from collections import namedtuple
from datetime import datetime, timedelta
from requests import HTTPError
from dateutil import parser

import requests
import json
import logging
import base64

log = logging.getLogger(__name__)


ACCESS_TOKEN_EXPIRATION_COEFFICIENT = 0.8


Catalog = namedtuple(
    'Catalog', 
    ('name', 'logo', 'approvalStatus', 'catalogAccountID', 'productCount', 'skuCount', 'lastPublishedDate', 'hasInventory', 'hasDropship', 'id')
)


class API():
    __slots__ = '_access_token', 'access_token_expires_at', 'username', 'password', '__dict__'
    
    def __init__(self, username='', password='') -> None:
        self.username = username
        self.password = password
        self._access_token = False
        self.access_token_expires_at = datetime.now()

    def set_access_token_expiry_datetime(self, seconds=120):
        delta = timedelta(seconds=seconds*ACCESS_TOKEN_EXPIRATION_COEFFICIENT)
        self.access_token_expires_at = datetime.now() + delta
        log.debug(f'Access token is set to expire at {self.access_token_expires_at}')

    def refresh_access_token(self):
        response = requests.post(
            'https://ccm.sellerscommerce.com/gateway/gettoken',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            },
            json={
                'username': self.username,
                'password': self.password
            }
        )
        response.raise_for_status()

        payload = json.loads(response.content)
        credentials = namedtuple("Credentials", payload.keys())(*payload.values())
        self._access_token = credentials.access_token
        self.token_expiration = self.set_access_token_expiry_datetime(
            seconds=credentials.expires_in
        )

    @property
    def is_access_token_expired(self):
        return not self._access_token or datetime.now() > self.access_token_expires_at

    @property
    def access_token(self):
        if self.is_access_token_expired:
            log.debug('Expired access token')
            self.refresh_access_token()

        return self._access_token

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

    def catalogs(self):
        headers = self.headers
        log.info(f'Fetch list of product catalogs')
        response = requests.get(
            'https://ccm.sellerscommerce.com/gateway/product/getcatalogs.json',
            headers=headers
        )

        response.raise_for_status()

        data = json.loads(response.content)

        for item in data:
            # Parse dates.
            last_published_date = item.get('lastPublishedDate', False)
            item['lastPublishedDate'] = parser.parse(last_published_date) \
                if last_published_date \
                else False

        catalog_objects = [Catalog(*item.values()) for item in data]
        return catalog_objects


def download_image(url, encode_base64=False):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        
        if encode_base64:
            return base64.b64encode(response.content)
        
        return response.content
    except:
        return False
