import os
import time
from xml_parser import xml_parse
from api_request import api_parse
from env import ARCHIVE_PATH

__location__  = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
remove_illegal_char_map = dict((ord(char), '_') for char in '/\*?:"<>|')

def archive(data):
    channel = data['channel'].translate(remove_illegal_char_map)
    title = data['title'].translate(remove_illegal_char_map)
    t = time.strftime('%Y-%m-%d_%H-%M-%S')
    if not os.path.exists(ARCHIVE_PATH + channel):
        os.makedirs(ARCHIVE_PATH + channel)
    output_location = ARCHIVE_PATH + channel + "\\" + t + "_" + title + "_" + data['id'] + ".mp4"
    youtube_link = "https://www.youtube.com/watch?v=" + data['id']
    cmd = "streamlink --hls-live-restart -o \"" + output_location + "\" " + youtube_link + " best"
    os.system("start cmd /k "+cmd)

while True:
    monitor_list = []
    request_list = ''
    videos = set()
    t_videos = set()
    t = time.gmtime(0)
    
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
    
    print("Polling\n")
    for channel in monitor_list:
        xml_data = xml_parse(channel)
        for video in xml_data['videos']:
            if video not in videos:
                request_list += video+','
            else:
                t_videos.add(video)
    
    api_data = api_parse(request_list)
    if len(api_data) > 0:
        for data in api_data:
            if data['live'] == 'none':
                t_videos.add(data['id'])
            elif data['live'] == 'upcoming':
                print(data['channel'],':',data['id'],":",data['live'],data['schedule'],":",data['title'])
            elif data['live'] == 'live':
                print(data['channel'],':',data['id'],":",data['live'],":",data['title'])
                archive(data)
                t_videos.add(data['id'])
    
    if videos != t_videos:
        videos = t_videos
        with open(os.path.join(__location__,"videos.txt"),'w') as f:
            for video in videos:
                f.write(video+'\n')
            f.close()
    
    print("\nWaiting...")
    time.sleep(60)
