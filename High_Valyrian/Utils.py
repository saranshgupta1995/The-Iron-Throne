import re

def strip_search(txt, data={}):
    txt = re.sub('[!?,.]', '', txt.lower())
    txt=[wrd for wrd in set(txt.split()) if (len(wrd)>3 and (wrd not in data))]
    return txt
