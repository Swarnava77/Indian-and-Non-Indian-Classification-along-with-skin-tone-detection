import urllib.request
from bs4 import BeautifulSoup
import re
from pytube import YouTube 

query = input("Enter the thing you wanna search for: ")
query= query.split()
query='+'.join(query)
searchurl = 'https://www.youtube.com/results?search_query=' + query


html = urllib.request.urlopen(searchurl)
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())     

n = int(input("Enter the number of videos to download: "))

#link of the video to be downloaded 
name = 1
for i in range(n):
  link=("https://www.youtube.com/watch?v=" + video_ids[i])
  try: 
    yt_obj=YouTube(link)
    filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
    filters.get_lowest_resolution().download()
    name+=1
  except:
    print("Connection Error")
  