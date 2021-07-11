from collections import namedtuple
from datetime import datetime, timedelta
from requests import HTTPError
from dateutil import parser

import requests
import json
import logging
import base64
import hashlib


log = logging.getLogger(__name__)


ACCESS_TOKEN_EXPIRATION_COEFFICIENT = 0.8


Catalog = namedtuple(
    'Catalog', 
    (
        'name', 
        'logo', 
        'approvalStatus', 
        'catalogAccountID', 
        'productCount', 
        'skuCount', 
        'lastPublishedDate', 
        'hasInventory', 
        'hasDropship', 
        'id', 
        'hash'
    )
)

Category = namedtuple(
    'Category', 
    (
        'name',
        'image',
        'code',
        'categoryPath',
        'categoryCodePath',
        'parentID',
        'categoryIDPath',
        'id',
        'hash'
    )
)

Product = namedtuple(
    'Product', 
    (
        'catalogID', 
        'supplierName', 
        'productName', 
        'productCode', 
        'thumbnailImage', 
        'largeImage', 
        'description',
        'technicalSpecification',
        'additionalInformation',
        'msrp',
        'map',
        'costPrice',
        'sortOrder',
        'width',
        'height',
        'length',
        'brandName',
        'brandImage',
        'videoPath',
        'status',
        'sizeChart',
        'categories',
        'id',
        'images',
        'hash'
    )
)


def download_image(url, encode_base64=False):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        
        if encode_base64:
            return base64.b64encode(response.content)
        
        return response.content
    except:
        return False


def dict_hash(d):
    hash_object = hashlib.md5(json.dumps(d).encode())
    return hash_object.hexdigest()


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
            hash = dict_hash(item)

            # Parse dates.
            last_published_date = item.get('lastPublishedDate', False)
            last_published_date = parser.parse(last_published_date) \
                if last_published_date \
                else False
            item.update({
                'lastPublishedDate': last_published_date,
                'hash': hash
            })

        catalog_objects = [Catalog(*item.values()) for item in data]
        return catalog_objects

    def products(self, catalog_id, product_count=2000, batch_size=500):
        base_url = 'https://ccm.sellerscommerce.com/gateway/product/getproducts.json'

        # Use generator.
        upper_bound = product_count \
            if product_count % batch_size == 0 \
            else product_count + batch_size

        product_data = []

        # TODO delete comment.
        # for batch_count in range(0, upper_bound, batch_size):
        for batch_count in range(0, 1):
            headers = self.headers

            # Reached the end page.
            if batch_count > product_count:
                break

            url = f'{base_url}/{catalog_id}/{batch_count}/{batch_size}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = json.loads(response.content)

            for item in data:
                hash = dict_hash(item)

                categories = []
                for category in item.get('categories', []):
                    category['hash'] = dict_hash(category)
                    categories.append(
                        Category(*category.values())
                    )
                
                images_urls = item.get('largeImage', '')
                images = images_urls.split('|') if images_urls else []
                
                item.update({
                    'categories': categories,
                    'images': images,
                    'hash': hash
                })
                product_data.append(item)

        products_cleaned = [Product(*item.values()) for item in product_data]
        return products_cleaned
        

def main():
    username = "feury"
    password = "8eb47c07f0aa41fe9e0b94c44c723be4"
    api = API(username=username, password=password)
    products = api.products(40, 4229)
    a = 10


if __name__ == '__main__':
    main()
