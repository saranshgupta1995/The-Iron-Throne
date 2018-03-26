import pafy
import re, urllib, os, sys
import urllib2
import pyautogui

class Mel:
    
    def getYoutubeBestSearch(self,song):
        urlopen = urllib2.urlopen  # open a url
        encode = urllib.urlencode  # encode a search line
        retrieve = urllib.urlretrieve  # retrieve url info
        cleanup = urllib.urlcleanup()  # cleanup url cache
        query_string = encode({"search_query" : song})
        html_content = urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
        return ("https://www.youtube.com/watch?v="+search_results[0])


    def downloadAudioFrom(self,url):
        print(url)
        pafy.new(url).getbestaudio(preftype="m4a").download(quiet=True)

    def switchApp(self,num):
        pyautogui.keyDown('alt')
        for i in range(num):
            pyautogui.press('tab')
        pyautogui.keyUp('alt')
