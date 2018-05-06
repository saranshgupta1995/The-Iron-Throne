import itertools, re
from random import randint

def breakdown(sen):
    lst=sen.split()
    if(not len(lst)):
        return []
    combinatorics = itertools.product([True, False], repeat=len(lst) - 1)
    solution = []
    for combination in combinatorics:
        i = 0
        one_such_combination = [lst[i]]
        for slab in combination:
            i += 1
            if not slab:
                one_such_combination[-1] += ' '+lst[i]
            else:
                one_such_combination += [lst[i]]
        solution.append(one_such_combination)

    return solution[::-1]

def check_for_data(in_sen):
    cmd=''
    cmd_data=[]
    cmd_text=''
    is_data=False
    for i in range(len(in_sen)):
        if(in_sen[i]=='['):
            is_data=True
            continue
        elif(in_sen[i]==']'):
            is_data=False
            cmd_data+=[cmd_text]
            cmd_text=''
            continue
        if(is_data):
            cmd_text+=in_sen[i]
        else:
            cmd+=in_sen[i]
    return ' '.join([ c for c in cmd.split() if c]), cmd_data

def send_input(txt):
    with open('Citidel//Temp.txt','w') as f:
        f.write(str(randint(10000,99999))+txt)

def get_all_tags(self,text):
    text = nltk.word_tokenize(text)
    return nltk.pos_tag(text)


def find_meaning_in(in_sen,data_dict_top,data_dict_deep):
    for data_dict in (data_dict_top,data_dict_deep):
        combs=breakdown(in_sen)
        matches= ([comb for comb in combs if all(part in [j for i in data_dict.values() for j in i] for part in comb)])
        gists= [[key for part in x for key in data_dict.keys() if part in data_dict[key]] for x in matches]
        data={}
        for match in matches:
            for part in match:
                for key in data_dict.keys():
                    if part in data_dict[key]:
                        if(key not in data.get(part,[])):
                            data[part]=data.get(part,[])+[key]
        if(len(data)):
            d=[]
            for match in matches:
                s=[]
                for part in match:
                    s2=[]
                    for similar in data[part]:
                        if(len(s)):
                            s2+=[x+[similar] for x in s]
                        else:
                            s2+=[[similar]]
                    s=s2
                d+=[' '.join(x) for x in s]
            found =list(set(d))

            for key in data_dict_top:
                for value in data_dict_top[key]:
                    if found.count(value)>0:
                        return key
    return ''

def strip_search(txt,stop_words=[]):
    txt = re.sub('[!?,.]', '', txt)
    txt=' '.join([wrd for wrd in txt.split() if wrd not in stop_words])
    return txt
