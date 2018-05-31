import os, pickle
from Bran import Weirwood

## Make Logger Folder
try:
    os.mkdir('Logger')
except:
    pass


# pickle.dump({},open('Citidel//vocab','wb'))



w=Weirwood.Weirwood()

w.drives=[x+':\\' for x in input("Which drives do you want monitor? Enter you commonly used drives and avoid drives with too many software installation. Eg - to monitor drives D, E,F , enter 'D E F' ").split()]

w.capture_data()
