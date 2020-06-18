import urllib3
import xmltodict
    
def xml_parse(id):
    data = None
    output = None
    http = urllib3.PoolManager()
    try:
        response = http.request('GET',"https://www.youtube.com/feeds/videos.xml?channel_id="+id)
        data = xmltodict.parse(response.data)
        feed = data['feed']
        title = feed['title']   #channel name
        if "entry" in feed:
            entry = feed['entry']   #videos
            
            output = {}
            output['channel'] = title
            output['videos'] = set()

            for video in entry:
                v = video['yt:videoId']
                output['videos'].add(v)
    except:
        print("Failed to parse xml from response, id: "+id)
    
    return output
