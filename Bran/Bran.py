import os, pickle

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
        self.conflict=False
        try:
            self.__world=pickle.load(open((os.path.join(os.getcwd(),'Varys','datadict.p')),"rb"))
        except:
            self.__world=pickle.load(open((os.path.join(os.getcwd(),'..','Varys','datadict.p')),"rb"))
        print ('Bran loaded')

    def show_glimpse(self, target):
        return self.__world.get(target,['location missing'])

    def choose_tree(self, target):
        if(len(self.show_glimpse(target))==1):
            self.tree.tree=[branch for branch in self.show_glimpse(target)[0].split('\\') if branch]+[target]
        else:
            self.conflict=True
            self.tree.all_leaves=[os.path.join(x,target) for x in self.show_glimpse(target)]

    def get_all_parents(self, target):
        return self.tree.tree

    def get_parent(self,target):
##        if(len(self.tree)):
##            parent = '\\'.join(self.tree)
##            parent+='\\'*('\\' not in parent)
##            return parent
        if('\\' in target):
            parent='\\'.join([x for x in self.get_path(target).split('\\') if x][:-1])
        else:
            parent = '\\'.join(self.get_all_parents(target))
        parent+='\\'*('\\' not in parent)
        return parent

    def previous_folder(self, target):
        return self.get_parent(target)

    def readfoldersin(self, path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def readfilesin(self, path):
        return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

    def readPath(self, path):
        try:
            data = [d for d in os.listdir(path)]
        except:
            data=[]
        finally:
            return data


    def get_path(self,target):
        if(len(self.tree)):
            return os.path.join('\\'.join(self.tree),target)
        return os.path.join(self.show_glimpse(target)[0],target)

    def locate(self, target):
        if(len(self.show_glimpse(target))==1):
            return self.readPath(self.show_glimpse(target)[0])
        else:
            return self.show_glimpse(target)

    def peek_inside(self, target):
        if(len(self.tree.tree)):
            data=self.readPath(os.path.join('\\'.join(self.tree.tree),target))
            return data
        if(len(self.show_glimpse(target))==1):
            data= self.readPath(self.get_path(target))
        else:
            data= self.show_glimpse(target)
            data=[x+'\\'+target for x in data]
            data=['\\'.join([y for y in x.split('\\') if y]) for x in data]
        return data

    def get_inside(self,target):
        target=os.path.join(self.tree.cwd,target)
        os.startfile(target)
