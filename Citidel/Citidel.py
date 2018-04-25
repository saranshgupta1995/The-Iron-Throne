import json, os, shelve, threading, time, pygame, pyautogui, sys
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
pyautogui.PAUSE = 0

## TODO shift + dir to select text bug

## Left Joystick : mouse movement
## Right Joystick : arrow keys
## L1 : Left Shift
## L2 : Left Ctrl
## R1 : tab
## R2 : alt
## 3 : mouse left click
## 4 : mouse right click
## Start : Enter
## Select : Backspace

class Citidel:

    def __init__(self):
        self.__pressed_s_c=[0,0]
        self.__pressed_a_t=[0,0]
        self.get_joystick()
        self.loadData()
        print ('Citidel loaded')

    def get_joystick(self):
        self.useGamepad=True
        pygame.init()
        try:
            self.__j = pygame.joystick.Joystick(0)
            self.__j.init()
        except:
            self.__j=None
            self.useGamepad=False

    def loadData(self):
        a=time.time()
        self.info_data=''
        self.consts = json.loads(open('Citidel//consts.json').read())
        self.cmds = json.loads(open(self.consts['cmds_path']).read())
        self.stop_words=json.loads(open(self.consts['filter_path']).read())['stop words']
        self.convs_deep=json.loads(open(self.consts['conv_deep_path']).read())
        self.open_convs()
        with open(self.consts['time_log_path'], 'a') as fp:
            fp.write('\nCitidel Data Time Log-'+str(time.time()-a))

    def open_convs(self,character='tyrion',mode='in'):
        self.convs_in=json.loads(open(self.consts['conv_in_path']).read())
        self.convs_out=json.loads(open('Citidel//'+character+'_conversations_out'+'.json').read())

    def close_convs(self,character='tyrion',mode='in'):
        with open('Citidel//conversations_'+mode+'.json', 'w') as fp:
            json.dump(self.convs_in, fp)

    def add_convs(self, for_data, value):
        citidel.convs_in[for_data]=citidel.convs_in.get(for_data,[])+[value]

    def key_debounce(self,mul=1):
        time.sleep(self.consts['debounce_base']*mul)

    def check_gamepad(self):
        responsivity=self.consts['sensitivity']
        out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        it = 0
        pygame.event.pump()


        for i in range(0, self.__j.get_numaxes()):
            out[it] = self.__j.get_axis(i)
            if(-0.8<out[it]<0.8):
                out[it]*=0.3
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
        elif(self.__pressed_s_c[0]):
            pyautogui.keyUp('shiftleft')
            self.__pressed_s_c[0]=0
        if(out[9]):
            pyautogui.press('tab')
            self.key_debounce(self.consts['debounce_mid_mul'])
        if(out[10]):
            if(not self.__pressed_s_c[1]):
                pyautogui.keyDown('ctrlleft')
                self.__pressed_s_c[1]=1
        elif(self.__pressed_s_c[1]):
            pyautogui.keyUp('ctrlleft')
            self.__pressed_s_c[1]=0

        if(out[11]):
            if(not self.__pressed_a_t[1]):
                pyautogui.keyDown('alt')
                self.__pressed_a_t[1]=1
        elif(self.__pressed_a_t[1]):
            pyautogui.keyUp('alt')
            self.__pressed_a_t[1]=0

        if(out[12]):
            pyautogui.press('backspace')
            self.key_debounce(self.consts['debounce_mid_mul'])

        if(out[13]):
            pyautogui.press('enter')
            self.key_debounce(self.consts['debounce_mid_mul'])

        if(out[6]):
            pyautogui.click(button='left')
            self.key_debounce(self.consts['debounce_mid_mul'])
        if(out[7]):
            pyautogui.click(button='right')
            self.key_debounce(self.consts['debounce_mid_mul'])
        return dire
