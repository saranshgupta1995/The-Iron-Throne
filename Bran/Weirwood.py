import os,pickle
import random

class Weirwood:

    def __init__(self):
        self.data={}
        self.surveyed={}
        self.drives=['F:\\']
        self.orig_path=os.getcwd()
        self.filtered_folders=['node_modules','$RECYCLE.BIN','maildir']
        self.mode='collect'

    def add_data(self,parent, child):
        if(random.randint(10, 10**7)<30):
            print parent
        parent=parent.lower()
        child=child.lower()
        if(self.mode=='collect'):
            self.data[child]=self.data.get(child,[])+[parent]
        elif(self.mode=='new_survey'):
            if(parent not in self.data.get(child,[])):
                self.surveyed[child]=self.surveyed.get(child,[])+[parent]


    def get_folders(self,path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def get_files(self,path):
        return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

    def get_data(self,path):
        if(len(self.get_files(path))<1000):
            [self.add_data(path, f) for f in self.get_files(path) if not f.startswith('.')]
        for folder in self.get_folders(path):
            if not folder.startswith('.'):
                if not folder in self.filtered_folders:
                    self.add_data(path, folder)
                    new_path=os.path.join(path, folder)
                    if(os.path.isdir(new_path)):
                        try:
                            self.get_data(new_path)
                        except:
                            print 'failed to capture data for '+folder

    def new_survey(self, data):
        self.surveyed={}
        self.mode='new_survey'
        # try:
        #     x=open("Citidel//datadict.p","rb")
        # except:
        #     x=open("datadict.p","rb")
        # self.data = pickle.load(x)
        # x.close()
        self.data=data
        self.fly()
        return [value+'\\'+key for key in self.surveyed.keys() for value in self.surveyed[key]]

    @property
    def survey_len(self):
        return sum([len(x) for x in self.surveyed.values()])

    def save_survey_data(self, data=None):
        self.mode='collect'
        if(not data):
            for key in self.surveyed.keys():
                for value in self.surveyed[key]:
                    self.add_data(value, key)
        else:
            for key in data.keys():
                self.add_data(data[key], key)
        return self.remember_data()

    def remember_data(self):
        os.chdir(self.orig_path)
        try:
            pickle.dump(self.data,open("Citidel//datadict.p","wb"))
        except:
            pickle.dump(self.data,open("datadict.p","wb"))
        return self.data

    def save_this_branch(self,branch):
        branch=[x for x in branch.split('\\') if x]
        branch, leaf='\\'.join(branch[:-1]), branch[-1]
        branch={leaf:branch}
        self.mode='new_survey'
        temp_survey_data={}
        for key in self.surveyed.keys():
            temp_survey_data[key]=[]+self.surveyed[key]
        self.surveyed={}
        for key in temp_survey_data.keys():
            for value in temp_survey_data[key]:
                if key not in branch.keys():
                    self.add_data(value, key)

        data=self.save_survey_data(branch)
        return data, [value+'\\'+key for key in self.surveyed.keys() for value in self.surveyed[key]]

    def capture_data(self):
        self.mode='collect'
        self.fly()
        self.remember_data()

    def fly(self):
        for drive in self.drives:
            self.get_data(drive)
