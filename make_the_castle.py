import os, pickle
from Bran import Weirwood

## Make Logger Folder
try:
    os.mkdir('Logger')
except:
    pass


pickle.dump({},open('Citidel//pika.p','wb'))

Weirwood().capture_data()
