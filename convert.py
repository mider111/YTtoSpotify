#TODO 1. Get YT playlist and video titles ----- DONE
#TODO 2. Log in spotify and create empty playlist
#TODO 3. Convert playlist

from googleapiclient.discovery import build
import os

youtube_token = os.environ.get('YT')


def get_playlist_videos(yt_api_token, playlist_id):
    youtube = build('youtube', 'v3', developerKey=yt_api_token)

    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id
    )

    pl_response = pl_request.execute()

    videos = []
    for item in pl_response['items']:
        videos.append(item['contentDetails']['videoId'])

    v_request = youtube.videos().list(
        part='contentDetails, snippet',
        id=','.join(videos)
    )
    v_response = v_request.execute()

    for item in v_response['items']:
        print(item['snippet']['title'] )


def main():
    get_playlist_videos(youtube_token, 'PLxA687tYuMWjuNRTGvDuLQZjHaLQv3wYL')


if __name__ == "__main__":
    main()
