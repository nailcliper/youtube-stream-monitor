#youtube api parameters
#https://developers.google.com/youtube/v3/docs/videos/list#http-request

from apiclient.discovery import build
from env import YOUTUBE_API_KEY

youtube_api_key = YOUTUBE_API_KEY
youtube = build("youtube","v3",developerKey=youtube_api_key)

def api_parse(video_ids):
    api_data = []
    req = youtube.videos().list(
        part='snippet,liveStreamingDetails',
        id=video_ids
    )
    try:
        response = req.execute()
        if len(response['items']) > 0:
            for item in response['items']:
                data = {}
                
                snippet = item['snippet']
                data['title'] = snippet['title']
                data['channel'] = snippet['channelTitle']
                data['live'] = snippet['liveBroadcastContent']
                data['id'] = item['id']
                
                if("liveStreamingDetails" in item):
                    data['schedule'] = item['liveStreamingDetails']['scheduledStartTime']
                else:
                    data['schedule'] = ''
                api_data.append(data)
    except:
        print("No response from API request")
    return api_data
