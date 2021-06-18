#!/usr/bin/python3

import requests
import time


class YaUploader:

    URL = 'https://cloud-api.yandex.net/v1/disk'
    date = time.strftime('%d%m%Y_%H%M%S')
    main_folder = 'backup_photos_social'
    def __init__(self, token, folder_social_network, user_folder, album_folder):
        self.folder_social_network = folder_social_network
        self.user_folder = user_folder
        self.album_folder = album_folder
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token
        }

    def disk_info(self):
        url = self.URL
        headers = self.headers
        response = requests.get(url, headers=headers)
        return response.json()

    def _create_folder(self):
        url = self.URL + '/resources'
        headers = self.headers
        create_folder = [
        self.main_folder,
        self.folder_social_network,
        self.user_folder,
        self.album_folder,
        self.date
        ]

        path_to_folder = ''
        for folder in create_folder:
            path_to_folder += f'{folder}/'
            params = {'path': path_to_folder, 'overwrite': 'true'}
            requests.put(url=url, headers=headers, params=params)

        return path_to_folder

    def _path_to_file(self, file_name):
        url = self.URL + '/resources/upload'
        folder = self._create_folder()
        headers = self.headers
        params = {'path': f'{folder}/{file_name}', 'overwrite': 'true'}
        response = requests.get(url=url, headers=headers, params=params)

        return response.json()

    def upload(self, file_name):
        self._create_folder()
        href = self._path_to_file(file_name=file_name).get('href')
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print(
                f'Загрузка файла {file_name} в папку {self.folder_name} произведена успешно.'
                )

    def upload_social_network(self, file_name, link):
        url = self.URL + '/resources/upload'
        folder = self._create_folder()
        params = {
        'path': f'{folder}{file_name}',
        'url': link
        }

        response = requests.post(url=url, params=params, headers=self.headers)
        if response.status_code != 202:
            print(f'Ошибка на сервере. Код ошибки: {response.status_code}')
