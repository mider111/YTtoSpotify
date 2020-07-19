# TODO 1. Get YT playlist and video titles ----- DONE
# TODO 2. Log in spotify and create empty playlist
# TODO 3. Convert playlist
from pprint import pprint

from googleapiclient.discovery import build
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

youtube_token = os.environ.get('YT')


def get_playlist_videos(yt_api_token, playlist_id):
    youtube = build('youtube', 'v3', developerKey=yt_api_token)
    videos = []
    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        videos_ids = []
        for item in pl_response['items']:
            videos_ids.append(item['contentDetails']['videoId'])

        v_request = youtube.videos().list(
            part='contentDetails, snippet',
            id=','.join(videos_ids)
        )
        v_response = v_request.execute()

        for item in v_response['items']:
            videos.append(item['snippet']['title'])

        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    return videos


def create_spotify_playlist(username_id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

def clean_titles(videos):
    for v in videos: 

def main():
    videos = get_playlist_videos(youtube_token, 'PLxA687tYuMWjuNRTGvDuLQZjHaLQv3wYL')
    print(len(videos))
    print(videos)
    create_spotify_playlist('wwohpbbvy3sz9ul8fspapyp2o')


if __name__ == "__main__":
    main()
