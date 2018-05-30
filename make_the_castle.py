import os, pickle
from Bran import Weirwood

## Make Logger Folder
os.mkdir('Logger')

pickle.dump({},open('Citidel//pika.p','wb'))

Weirwood().capture_data()
