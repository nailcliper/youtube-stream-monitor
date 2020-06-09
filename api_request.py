#youtube api parameters
#https://developers.google.com/youtube/v3/docs/videos/list#http-request

from apiclient.discovery import build
from env import YOUTUBE_API_KEY

youtube_api_key = YOUTUBE_API_KEY
youtube = build("youtube","v3",developerKey=youtube_api_key)

def api_parse(video_id):
    data = {}
    req = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    try:
        response = req.execute()
        if len(response['items']) > 0:
            snippet = response['items'][0]['snippet']
            data['title'] = snippet['title']
            data['channel'] = snippet['channelTitle']
            data['live'] = snippet['liveBroadcastContent']
            data['id'] = video_id
    except:
        print("No response from API request")
    return data
