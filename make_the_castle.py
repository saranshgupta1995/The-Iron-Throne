import os, pickle, json
from Bran import Weirwood

## Make Logger Folder
try:
    os.mkdir('Logger')
except:
    pass


drpx_need=False
consts=json.loads(open('Citidel//consts.json').read())
if(not drpx_need):
    consts['drpbx_cmds_file']="Citidel//waste.txt"
    consts['drpbx_exps_file']="Citidel//waste.txt"
    with open('Citidel//consts.json', 'w') as fp:
        json.dump(consts, fp)

w=Weirwood.Weirwood()

w.drives=[x+':\\' for x in raw_input("Which drives do you want monitor? Enter you commonly used drives and avoid drives with too many software installation. Eg - to monitor drives D, E,F , enter 'D E F' ").split()]

w.capture_data()
