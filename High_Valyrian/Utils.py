def strip_search(txt):
    txt = re.sub('[!?,.]', '', txt)
    txt=' '.join([wrd for wrd in txt.split() if len(wrd)>3])
    return txt.lower()
