import os
from googleapiclient.discovery import build
# import json


class Video:

    def __init__(self, video_id: str):
        self.__video_id = video_id
        self.__api_key = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__video = self.__youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()

        self.title = self.__video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.__video_id
        self.views = self.__video['items'][0]['statistics']['viewCount']
        self.likes = self.__video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
