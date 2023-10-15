import os

import googleapiclient.discovery
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.__api_key = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.__channel['items'][0]['snippet']['title']
        self.description = self.__channel['items'][0]['snippet']['description']
        self.video_count = self.__channel['items'][0]['statistics']['videoCount']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscribers = self.__channel['items'][0]['statistics']['subscriberCount']
        self.viewCount = self.__channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return googleapiclient.discovery

    def to_json(self, name):
        to_json = json.dumps({'id': self.__channel_id, 'title': self.title, 'description': self.description,
                              'vidoCount': self.video_count, 'url': self.url,
                              'subscribers': self.subscribers, 'viewCount': self.viewCount}, indent=2,
                             ensure_ascii=False)
        with open(name, 'w', encoding='UTF-8') as json_file:
            json_file.write(to_json)
