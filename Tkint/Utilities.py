import itertools

def breakdown(sen):
    lst=sen.split()
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

def send_input(txt):
    with open('Citidel//Temp.txt','w') as f:
        f.write(txt)

def get_all_tags(self,text):
    text = nltk.word_tokenize(text)
    return nltk.pos_tag(text)


def find_meaning_in(in_sen,data_dict_top,data_dict_deep):
    for data_dict in (data_dict_top,data_dict_deep):
        combs=breakdown(in_sen)
        gist= ([comb for comb in combs if all(part in [j for i in data_dict.values() for j in i] for part in comb)]+[' x x Placeholder x x '])[0]
        gist= [key for part in gist for key in data_dict.keys() if part in data_dict[key]]
        if(len(gist)):
            in_sen=' '.join(gist)
            print in_sen
            for key in data_dict_top:
                for value in data_dict_top[key]:
                    if value==in_sen:
                        return key
    return ''
