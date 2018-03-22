import Tkinter as Tk

class Face:

    def __init__(self):
        self.__window=Tk.Tk()
        self.__window.title("The Iron Throne")
        self.__window.geometry("300x400")
        self.__labels=[]
        self.__textBox=Tk.Entry(self.__window)
        self.__textBox.pack()
        self.__buttons=[]
        self.__cmd=""
        
##        lbl=Tk.Label(window,text="Label 1")
##        lbl.pack()
##        lbl1=Tk.Label(window,text="Label 21")
##        lbl1.pack()
##        ent=Tk.Entry(window)
##        ent.pack()
##        btn=Tk.Button(window,text="Btn")
##        btn.pack()

    def take_Input(self):
        self.__cmd=">"
        while self.__cmd[-1]!="<":
            self.__cmd=">"+self.__textBox.get()
            self.__window.update_idletasks()
            self.__window.update()
        return self.__cmd[1:-1]
        
    def add_label(self,txt):
        self.__labels+=[Tk.Label(self.__window,text=txt)]
        self.__labels[len(self.__labels)-1].pack()

    def removeUI(self):
        self.__window.destroy()
        
if __name__=="__main__":
    d=Face()
    d.add_label("Pikachu")
    inp=d.take_Input()
    d.removeUI()
