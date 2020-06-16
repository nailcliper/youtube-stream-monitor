import os
import time
from datetime import datetime
from dateutil import tz
from xml_parser import xml_parse
from api_request import api_parse
from env import ARCHIVE_PATH

__location__  = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
remove_illegal_char_map = dict((ord(char), '_') for char in '/\*?:"<>|')
utcz = tz.tzutc()
localz = tz.tzlocal()
t = datetime.now().replace(microsecond=0)

def archive(data):
    channel = data['channel'].translate(remove_illegal_char_map)
    title = data['title'].translate(remove_illegal_char_map)
    start = t.strftime('%Y-%m-%d_%H-%M-%S')
    if not os.path.exists(ARCHIVE_PATH + channel):
        os.makedirs(ARCHIVE_PATH + channel)
    output_location = ARCHIVE_PATH + channel + "\\" + start + "_" + title + "_" + data['id'] + ".mp4"
    youtube_link = "https://www.youtube.com/watch?v=" + data['id']
    cmd = "streamlink --hls-live-restart -o \"" + output_location + "\" " + youtube_link + " best"
    os.system("start cmd /k "+cmd)

while True:
    monitor_list = []
    request_list = ''
    videos = set()
    t_videos = set()
    t = datetime.now().replace(microsecond=0)
    
    with open(os.path.join(__location__,"monitor_list.txt"),'r') as f:
        for line in f:
            line = line.strip()
            if line[0] != '#':
                line = line.split()
                monitor_list.append(line[0])
        f.close()
    
    with open(os.path.join(__location__,"videos.txt"),'r') as f:
        for line in f:
            line = line.strip()
            videos.add(line)
        f.close()
    
    print("Polling",t,'\n')
    for channel in monitor_list:
        xml_data = xml_parse(channel)
        if xml_data:
            for video in xml_data['videos']:
                if video not in videos:
                    request_list += video+','
                else:
                    t_videos.add(video)
    
    api_data = api_parse(request_list) if request_list != '' else []
    if len(api_data) > 0:
        api_data = sorted(api_data, key=lambda k: k['schedule'])
        for data in api_data:
            if data['live'] == 'none':
                print(data['channel'],'\t:',data['id'],": Uploaded Video      :",data['title'])
                t_videos.add(data['id'])
            elif data['live'] == 'upcoming':
                schedule = datetime.fromisoformat(data['schedule'][:-1]).replace(tzinfo=utcz)
                schedule = schedule.astimezone(localz).replace(tzinfo=None)
                print(data['channel'],'\t:',data['id'],":",schedule,":",data['title'])
            elif data['live'] == 'live':
                print(data['channel'],'\t:',data['id'],": Live Now!           :",data['title'])
                archive(data)
                t_videos.add(data['id'])
    else:
        print("No Streams Found")
    
    if videos != t_videos:
        videos = t_videos
        with open(os.path.join(__location__,"videos.txt"),'w') as f:
            for video in videos:
                f.write(video+'\n')
            f.close()
    
    print("\nWaiting...")
    time.sleep(60)
