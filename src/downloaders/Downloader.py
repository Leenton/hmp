from xml.etree import ElementTree
import requests


def fetchRSS():
    #Function gets the latest video fron the content creator specified and adds it to the today array
    videos = []
    url = 'https://www.relay.fm/cortex/feed'
    response = requests.get(url)
    xmlrss = ElementTree.fromstring(response.content)

    print(xmlrss.tag)
    # print(xmlString)
    # for child in xmlString:
    #     for char in child.findall("{http://www.youtube.com/xml/schemas/2015}videoId"):
    #         videos.append(char.text)
    return videos

print(fetchRSS())

#load the individual python scripts for each podcast. 


#make a webrequest to the relevant websites to check if they need to be downloaded. 

#make a webrequest to check if new podcasts exist. 

#download the new podcast episodes we downloaded. 



# updates = podcasts.get_updates()

# for podcast in updates:
#     podcast.download()
#     podcast.injest()

