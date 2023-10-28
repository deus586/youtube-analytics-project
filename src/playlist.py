import os
from googleapiclient.discovery import build
import json
import datetime


class PlayList:
    format_time = 'PT%HH%MM%SS'
    sum_time = datetime.timedelta(hours=0, minutes=0, seconds=0)

    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        self.__api_key = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__playlist = self.__youtube.playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.__playlist_vids = (self.__youtube.playlistItems().
                                list(playlistId=self.__playlist_id, part='snippet,contentDetails').execute())
        self.__ids = []
        self.__likes = []
        for item in self.__playlist_vids['items']:
            video_id = item["snippet"]['resourceId']['videoId']

            self.__ids.append(video_id)

            # print(video_id)
            video = self.__youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
            # print(video)
            self.__likes.append(int(video['items'][0]['statistics']['likeCount']))
            duration = video['items'][0]['contentDetails']['duration']
            if 'H' not in duration:
                duration = 'PT0H' + duration[2:]
            if 'S' not in duration:
                duration += '0S'
            hours = datetime.datetime.strptime(duration, self.format_time).hour
            minutes = datetime.datetime.strptime(duration, self.format_time).minute
            seconds = datetime.datetime.strptime(duration, self.format_time).second
            self.sum_time += datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        self.total_duration = self.sum_time
        self.title = self.__playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.__playlist_id

    def show_best_video(self):
        return 'https://youtu.be/' + self.__ids[self.__likes.index(max(self.__likes))]

    def __str__(self):
        return str(self.sum_time)
