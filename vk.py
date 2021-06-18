#!/usr/bin/python3

import requests
import time


class Vk:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token, version):

        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.visitor = requests.get(self.URL + 'stats.trackVisitor', self.params)
        owner_id = requests.get(self.URL + 'users.get', self.params)
        self.owner_id = owner_id.json()['response'][0]['id']

    def user_info(self):

        user_url = self.URL + 'users.get'
        user_id = input(
           'Введите id пользователя, или его короткое имя (screen_name).\n'
           'Для текущего пользователя оставьте поле пустым нажав Enter: '
            )
    
        if user_id == '':
            user_id = self.owner_id
        
        user_params = {
            'user_ids': user_id,
            'fields': 'screen_name'
        }
        params = {**self.params, **user_params}
        response = requests.get(user_url, params).json()

        if 'error' in response.keys():
            error_code = response['error']['error_code']
            print(f'Произошла ошибка. Код ошибки: {error_code}.')
            print('='*77 + '\n')
            self.user_id = None

            return self.user_id

        try:
            self.first_name = response['response'][0]
        except IndexError:
            print(
                f'Пользователь {user_id} не найден. Либо Вы ошиблись при вводе.'
                )
            print('='*77 + '\n')
            self.user_id = None

            return self.user_id

        else:
            first_name = response['response'][0]['first_name']
            last_name = response['response'][0]['last_name']
            self.user_id = response['response'][0]['id']
            self.user_name = f'{first_name} {last_name}'

            if 'screen_name' in response['response'][0].keys():
                self.screen_name = response['response'][0]['screen_name']
                print(
                    f'Найден пользователь {self.user_name} id: {self.user_id}\n'
                    f'Короткое имя пользователя (screen_name): {self.screen_name}\n'
                )
                print('='*77 + '\n')

                return self.user_name, self.user_id, self.screen_name
            else:
                print(
                    f'Найден пользователь {self.user_name} id: {self.user_id}\n'
                    f'Короткого имени пользователя (screen_name) нет.\n'
                )
                print('='*77 + '\n')

                return self.user_name, self.user_id

    def albums(self):

        self.user_info()

        if self.user_id is None:
            print('Введенны некорректные данные')

        albums_url = self.URL + 'photos.getAlbums'
        albums_params = {
            'owner_id': self.user_id,
            'need_system': 1,
        }

        params = {**self.params, **albums_params}
        response = requests.get(albums_url, params).json()
        self.stop = 'nostop'

        try:
            count_albums = response['response']['count']
        except KeyError:
            print('Доступные альбомы не обнаружены. Либо доступ запрещён.')
            self.stop = 'stop'
            return self.stop

        else:            
            count_albums = int(response['response']['count'])
            items = response['response']['items']

            if count_albums == 1:
                print('Доступен один альбом:\n')

            elif 2 <= count_albums <= 4:
                print(f'Доступно {count_albums} альбома:\n')

            else:
                print(f'Доступно {count_albums} альбомов:\n')

            self.albums_title = {}
            for item in items:
                print(
                    f"'{item['title']}', ID альбома: {item['id']}, количество фотографий: {item['size']}."
                    )
                self.albums_title[item['id']] = item['title']

            print('='*77 + '\n')  
            return response, self.albums_title

    def photos_get(self):

        self.albums()

        if self.stop != 'stop':
            album_id = input(
                f"Введите id альбома, по умолчанию будет сохранён '{self.albums_title[-6]}': "
                )
            if album_id == '':
                album_id = -6
            count = input(
                'Введите количество фотографий, которые хотите сохранить.\n'
                'По умолчанию будет сохранено 5 фотографий: '
                )
            if count == '':
                count = 5

            photos_params = {
                'owner_id': self.user_id,
                'album_id': album_id,
                'rev': 0,
                'extended': 1,
                'count': count
            }

            photos_url = self.URL + 'photos.get'
            params = {**self.params, **photos_params}
            response = requests.get(photos_url, params).json()
            self.album_title = self.albums_title[int(album_id)]
            return response

        else:
            return 'continue'

    def photos_info(self):

        response = self.photos_get()
        if response == 'continue':
            pass

        else:
            if 'error' in response.keys():
                error_code = response['error']['error_code']
                print(f'Произошла ошибка. Код ошибки: {error_code}')
                return

            else:
                items = response['response']['items']
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
                    date_photo = time.strftime(
                        '%d%m%y', time.gmtime(item['date'])
                        )
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


            return photos_info, self.user_name, self.album_title
