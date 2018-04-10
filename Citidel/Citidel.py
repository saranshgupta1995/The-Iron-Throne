import json, os, shelve, threading, time, pygame, pyautogui, sys
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
pyautogui.PAUSE = 0

## Left Joystick : mouse movement
## Right Joystick : arrow keys
## L1 : Left Shift
## L2 : Left Ctrl
## 3 : mouse left click
## 4 : mouse right click
## Start : Enter
## Select : Backspace

class Citidel:

    def __init__(self):
        self.consts = json.loads(open('Citidel//consts.txt').read())
        self.cmds = json.loads(open('Citidel//cmds.txt').read())
        self.__pressed_s_c=[0,0]
        self.__pressed_a_t=[0,0]
        self.useGamepad=True
        self.open_convs()
        pygame.init()
        try:
            self.__j = pygame.joystick.Joystick(0)
            self.__j.init()
        except:
            self.useGamepad=False

    def getCmd(self):
        f=open((os.path.join(os.getcwd(),'Citidel','Temp.txt')),"r")
        t=f.read()
        f.close()
        return t

    def open_convs(self,character='tyrion',mode='in'):
        self.convs_in=json.loads(open('Citidel//'+character+'_conversations_in'+'.json').read())
        self.convs_out=json.loads(open('Citidel//'+character+'_conversations_out'+'.json').read())

    def close_convs(self,character='tyrion',mode='in'):
        with open('Citidel//'+character+'_conversations_'+mode+'.json', 'w') as fp:
            json.dump(self.convs_in, fp)

    def add_convs(self, for_data, value):
        citidel.convs_in[for_data]=citidel.convs_in.get(for_data,[])+[value]

    def key_debounce(self,mul=1):
        time.sleep(0.04*mul)

    def check_gamepad(self):
        responsivity=35
        out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        it = 0 #iterator
        pygame.event.pump()

        #Read input from the two joysticks
        for i in range(0, self.__j.get_numaxes()):
            out[it] = self.__j.get_axis(i)
            it+=1
        pyautogui.moveRel(out[0]*responsivity, out[1]*responsivity,duration=0.08)
        if(out[2]>0.9):
            pyautogui.press('right')
            self.key_debounce()
        if(out[3]>0.9):
            pyautogui.press('down')
            self.key_debounce()
        if(out[2]<-0.9):
            pyautogui.press('left')
            self.key_debounce()
        if(out[3]<-0.9):
            pyautogui.press('up')
            self.key_debounce()


        for i in range(0,self.__j.get_numhats()):
            dire=self.__j.get_hat(i)

        #Read input from buttons
        for i in range(0, self.__j.get_numbuttons()):
            out[it] = self.__j.get_button(i)
            it+=1

        if(out[8]):
            if(not self.__pressed_s_c[0]):
                pyautogui.keyDown('shiftleft')
                self.__pressed_s_c[0]=1
            else:
                pyautogui.keyUp('shiftleft')
                self.__pressed_s_c[0]=0
            self.key_debounce(10)
        if(out[9]):
            pyautogui.press('tab')
            self.key_debounce(6.5)
        if(out[10]):
            if(not self.__pressed_s_c[1]):
                pyautogui.keyDown('ctrlleft')
                self.__pressed_s_c[1]=1
            else:
                pyautogui.keyUp('ctrlleft')
                self.__pressed_s_c[1]=0
            self.key_debounce(10)
        if(out[11]):
            if(not self.__pressed_a_t[1]):
                pyautogui.keyDown('alt')
                self.__pressed_a_t[1]=1
            else:
                pyautogui.keyUp('alt')
                self.__pressed_a_t[1]=0
            self.key_debounce(10)

        if(out[12]):
            pyautogui.press('backspace')
            self.key_debounce(6.5)

        if(out[13]):
            pyautogui.press('enter')
            self.key_debounce(6.5)

        if(out[6]):
            pyautogui.click(button='left')
            self.key_debounce(6.5)
        if(out[7]):
            pyautogui.click(button='right')
            self.key_debounce(6.5)
        return dire

print ('Citidel loaded')
