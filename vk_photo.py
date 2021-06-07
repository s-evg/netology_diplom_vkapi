#!/usr/bin/python3

import requests
import time


class VkPhoto:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version):

        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.URL + 'users.get', self.params).json()['response'][0]['id']

    def photos_get(self, user_id=None):

        if user_id is None:
            user_id = self.owner_id

        photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'count': 100
        }

        photos_url = self.URL + 'photos.get'
        params = {**self.params, **photos_params}
        response = requests.get(photos_url, params).json()

        return response

    def photos_info(self):
        items = self.photos_get()['response']['items']
        photos_info = []
        info = {}
        likes_count = []
        repeat_likes_count = []

        for like in items:
            likes_count.append(like['likes']['count'])

        for like in likes_count:
            if likes_count.count(like) > 1:
                repeat_likes_count.append(like)

        for item in items:
            like = item['likes']['count']
            date_photo = time.strftime('%d%m%y', time.gmtime(item['date']))
            info = {
                'size': item['sizes'][-1]['type'],
                'link': item['sizes'][-1]['url']
            }

            if like in repeat_likes_count:
                info['file_name'] = f'{like}_{date_photo}.jpg'
                photos_info.append(info)

            else:
                info['file_name'] = f'{like}.jpg'
                photos_info.append(info)
                        
        return photos_info
