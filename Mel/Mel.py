import pafy
import re, urllib, os, sys
import urllib2
import pyautogui, pywinauto

pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
pyautogui.PAUSE = 0

class Mel:

    def __init__(self):
        print ('Mel reloaded')

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

    def switchApp(self,num=20):
        pyautogui.keyDown('alt')
        for i in range(num):
            pyautogui.press('tab')
        pyautogui.keyUp('alt')

    def get_info_on(self, se='https://duckduckgo.com/?q=', query='pikachu', incog=False,goo=False):
        if(goo):
            query='%21g '+query
        query=query.replace(' ','+')
        query=se+query
        app = pywinauto.Application(backend='uia')
        chrome_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        app.start(chrome_path + ' --force-renderer-accessibility '+('--incognito '*incog)+'--start-maximized '+query)



    def calculate_this(self,exp='0'):
        ans=0
        print('working on '+exp)
        try:
            ans=eval(exp)
        except:
            pass
        return str(ans)

if(__name__=='__main__'):
    m=Mel()
