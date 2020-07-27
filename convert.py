# TODO Get YT playlist and video titles ----- DONE
# TODO Clean titles. ----- DONE
# TODO Log in spotify and create empty playlist
# TODO Add songs to playlist

from googleapiclient.discovery import build
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import re

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
    spotify_token = util.prompt_for_user_token(
        username=username_id,
        scope="playlist-modify-public",
        client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI')
    )
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    sp.user_playlist_create(username_id, 'YouTube Converter PL', public=True, description='Test')


def clean_titles(videos):
    clean_list = []
    ''' IGNORE = ['(Music Video)', '(Official Music Video)', '(Audio)',
              '(Lyrics)', '[Official Audio]', '(Lyrics)', '(Official Video)',
              '(Lyric Video)', 'Lyrics', '[Official Music Video]',
              ] '''
    regex = '(\[|\().*(\]|\))'
    for v in videos:
        result = re.search(regex, v)
        if result:
            v = re.sub(regex, '', v)
            clean_list.append(v)
    return clean_list


def main():
    videos = get_playlist_videos(youtube_token, 'PLxA687tYuMWjuNRTGvDuLQZjHaLQv3wYL')
    print(len(videos))
    print(videos)
    create_spotify_playlist('wwohpbbvy3sz9ul8fspapyp2o')
    print(clean_titles(videos))


if __name__ == "__main__":
    main()
