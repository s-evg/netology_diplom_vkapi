#!/usr/bin/python3

from vk_photo import VkPhoto
from yauploader import YaUploader
from configuration import vk_token, user_id, version, ya_token
from pprint import pprint
import time


class BackupPhotoVk:

    def __init__(self, ya_token, vk_token, version):

        self.ya_agent = YaUploader(token=ya_token)
        self.vk_agent = VkPhoto(token=vk_token, version=version)
        self.photos_info = self.vk_agent.photos_info()

    def backup(self):

        c = 0
        for photo in self.photos_info:
            self.ya_agent.upload_vk_photo(file_name=photo['file_name'], link=photo['link'])
            time.sleep(1)
            c += 1

        print(f'Резервное копирование завершено. Сохранено {c} фотографий.')


if __name__ == '__main__':
    backup = BackupPhotoVk(ya_token=ya_token, vk_token=vk_token, version=version)
    backup.backup()
