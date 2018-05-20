import os, pickle
import Weirwood

class Tree:

    def __init__(self):
        self.tree=[]

    @property
    def cwd(self):
        parent = '\\'.join(self.tree)
        parent+='\\'*('\\' not in parent)
        return parent

    @property
    def parent(self):
        parent = '\\'.join(self.tree[:-1])
        parent+='\\'*('\\' not in parent)
        return parent

    def move_down_branch(self):
        self.tree=self.tree[:-1]

    def climb_up(self,target):
        if('\\' in target):
            self.tree=[x for x in target.split('\\') if x]
            return
        self.tree+=[target]

    @property
    def all_leaves(self):
        return [d for d in os.listdir(self.cwd)]
    def get_all_leaves(self):
        return [d for d in os.listdir(self.cwd)]

    @property
    def file_leaves(self):
        return [d for d in os.listdir(self.cwd) if not os.path.isdir(os.path.join(self.cwd, d))]

    @property
    def folder_leaves(self):
        return [d for d in os.listdir(self.cwd) if os.path.isdir(os.path.join(self.cwd, d))]

class Bran:

    def __init__(self):
        self.tree=Tree()
        self.weirwood=Weirwood.Weirwood()
        self.conflict=False
        try:
            self.__world=pickle.load(open((os.path.join(os.getcwd(),'Citidel//datadict.p')),"rb"))
        except:
            self.__world=pickle.load(open((os.path.join(os.getcwd(),'..','Varys','Citidel//datadict.p')),"rb"))
        print ('Bran loaded')

    def show_glimpse(self, target):
        return self.__world.get(target,['location missing'])

    def choose_tree(self, target):
        if(len(self.show_glimpse(target))==1):
            if(self.show_glimpse(target)[0]=='location missing'):
                self.tree.tree=['F:']
                return
            self.tree.tree=[branch for branch in self.show_glimpse(target)[0].split('\\') if branch]+[target]
        else:
            self.conflict=True
            self.tree.all_leaves=[os.path.join(x,target) for x in self.show_glimpse(target)]

    def readfoldersin(self, path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def readfilesin(self, path):
        return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

    def new_happenings(self):
        data=self.weirwood.new_survey(self.__world)
        return data

    def register_happenings(self):
        self.__world=self.weirwood.save_survey_data()

    def register_happening(self,happening):
        self.__world, new_found=self.weirwood.save_this_branch(happening)
        return new_found

    def get_path(self,target):
        if(len(self.tree.tree)):
            return os.path.join(self.tree.cwd,target)
        return os.path.join(self.show_glimpse(target)[0],target)

    def get_inside(self,target):
        target=os.path.join(self.tree.cwd,target)
        os.startfile(target)
