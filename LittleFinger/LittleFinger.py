import datetime, os, shelve
import openpyxl

##date_pointer: cell address of last date added
##entry_count: no of entries on date
##last_row: last entry of month
##total_exp: total expense in day/month
##daily_fixed_exp: prefixed expenses/day

## TODO add function to make new excel from pickle data in case data is corrupted
## TODO add function to make new pickle from excel
## TODO timeit and make code faster
## TODO add functions for statistical analysis
## TODO add error logger
## TODO check daily limits
## TODO convert everything to lowercase
## TODO add sum fields on top
## TODO add date processing drpbx file logs

class LittleFinger:

    def __init__(self,citidel=None):
        if(not citidel):
            from Citidel.Citidel import Citidel
            citidel=Citidel()
        self.__citidel=citidel
        self.__prefixed_expenses={'Mutual Funds':8000,'Medium Term Savings':2000,'Monthly Rent':5600}
        self.__BANKS=map(str,self.__citidel.consts['my_banks'])
        self.__WALLETS=map(str,self.__citidel.consts['my_wallets'])
        self.__xl_cols=self.__citidel.consts['lf_cols']
        self.__bank_name_col=str(self.__xl_cols['bank_name'])
        self.__date_col=str(self.__xl_cols['date'])
        self.__bank_det_col=str(self.__xl_cols['bank_details'])
        self.__bank_amount_col=str(self.__xl_cols['bank_amount'])
        self.__wallet_name_col=str(self.__xl_cols['wallet_name'])
        self.__wallet_details_col=str(self.__xl_cols['wallet_details'])
        self.__wallet_amount_col=str(self.__xl_cols['wallet_amount'])
        self.__cash_details_col=str(self.__xl_cols['cash_details'])
        self.__cash_amount_col=str(self.__xl_cols['cash_amount'])
        self.open_workbook()
        self.__current_date=str(self.__ws[self.__date_col+str(self.__shelf[self.getDate()[1]].get('date_pointer',3))].value)
        self.__day_diff=self.diff_in_days(datetime.date.today(),self.convert_to_date(self.__current_date))
        self.__insert_prefixed=False
        if self.__current_date !=self.getDate()[0]:
            self.__current_date,_=self.getDate()
            self.insert_new_date()
            self.__insert_prefixed=True
        self.__shelf[self.__current_date]=self.__shelf.get(self.__current_date,{})
        self.__shelf[self.__current_date]['entry_count']=self.__shelf[self.__current_date].get('entry_count',0)
        self.close_workbook()
        self.read_drpbx_logs()
        if(self.__insert_prefixed):
            self.add_log(sum(self.__prefixed_expenses.values())/(int(self.last_day_of_month().day))*(max(self.__day_diff,1))*(-1),'AX','prefixed expenses')
            self.__insert_prefixed=False
        print ('LittleFinger loaded')


    def set_month_limit(self):
        salary=self.__shelf[self.getDate()[1]].get('Income',0)
        self.__month_limit=salary
        self.__shelf[self.getDate()[1]]['daily_fixed_exp']=sum(self.__prefixed_expenses.values())/(int(self.last_day_of_month().day))
        self.__shelf[self.getDate()[1]]['exp_limit']=self.__month_limit/(int(self.last_day_of_month().day))

    def read_drpbx_logs(self):
        left_over=''
        with open(r'C:\Users\Saransh\Dropbox\Temps\Expenses.txt') as f:
            next_is_date=False
            for line in f:
                ## TODO Currently all file logs are pushed pushed to current data
                ## Push file expenses according to their date
                if(next_is_date):
                    ## To process
                    datetime.datetime.strptime(line, '%b %d %Y')
                    next_is_date=False
                if(line[:2]=="___"):
                    ## To process
                    next_is_date=True
                if(line[0] in ('+','-')):
                    am, trgt, det=line.split()
                    if('salary' in det.lower()):
                        self.add_salary(am,trgt)
                    else:
                        self.add_log(am,trgt,det)
                    continue
                if(line[0]=='$'):
                    am,src,trgt=line[1:].split()
                    self.do_transfer(am,src,trgt)
                    continue
                left_over+=line
            with open(r'C:\Users\Saransh\Dropbox\Temps\Expenses.txt', 'w') as fp:
                fp.write(left_over)

    def add_salary(self,amount, target):
        self.add_log(amount,target,'Income')
        self.open_workbook()
        self.__shelf[self.getDate()[1]]['Income']=int(amount)
        self.set_month_limit()
        self.close_workbook()

    def convert_to_date(self,str_date):
        if(str_date == 'None'):
            return datetime.date.today()
        y,m,d=[int(x) for x in str_date.split('-')]
        return datetime.date(y,m,d)

    def last_day_of_month(self,any_day=datetime.date.today()):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def diff_in_days(self, x, y=datetime.date.today()):
        return (x-y).days

    def print_headers(self):
        headers=self.__citidel.consts['headers']
        for col in range(len(headers)):
            self.__ws[chr(col+65)+'1']=str(headers[col])

    def open_workbook(self):
        self.__shelf=shelve.open('Citidel//exp_data',writeback=True)
        self.__wb = openpyxl.load_workbook('Citidel//Exp.xlsx')
        try:
            self.__ws=self.__wb[self.getDate()[1]]
        except KeyError:
            self.new_month_setup()

    def new_month_setup(self):
        self.__ws=self.__wb.create_sheet(title=self.getDate()[1])
        self.__shelf[self.getDate()[1]]={}
        self.__shelf[self.getDate()[1]]['total_exp']=0
        self.__shelf[self.getDate()[1]]['date_pointer']=3
        self.print_headers()

    def close_workbook(self):
        self.__wb.save('Citidel//Exp.xlsx')
        self.__shelf.close()

    def getDate(self):
        d=datetime.date.today()
        return str(d),str(d.month)+'-'+str(d.year)

    def add_log(self, amount, target, details):
        amount=int(amount)
        self.open_workbook()
        count_key=self.__shelf[self.__current_date].get('entry_count',0)+1
        d=self.__shelf[self.__current_date]
        self.__shelf[self.__current_date][count_key]=[target,amount,details]
        self.__shelf[self.__current_date]['entry_count']=count_key
        row=self.__shelf[self.getDate()[1]].get('date_pointer',3)
        if(target in self.__BANKS):
            mapping={
                self.__bank_name_col: target,
                self.__bank_det_col: details,
                self.__bank_amount_col: amount
                }
        elif(target in self.__WALLETS):
            mapping={
            self.__wallet_name_col: target,
            self.__wallet_details_col: details,
            self.__wallet_amount_col: amount
                }
        elif(target == 'CSH'):
            mapping={
            self.__cash_details_col: details,
            self.__cash_amount_col: amount
                }
        while(any([self.__ws[(key+str(row))].value for key in mapping])):
            row+=1
        for key in mapping:
            self.__ws[key+str(row)]=mapping[key]
        if(self.__current_date == str(self.last_day_of_month())):
            self.__shelf[self.__current_date]['last_row']=max([row,self.__shelf[self.__current_date].get('last_row',0)])
        self.__shelf[self.__current_date]['total_exp']-=amount
        self.__shelf[self.getDate()[1]]['total_exp']-=amount
        self.close_workbook()

    def insert_new_date(self):
        data_cols=[self.__cash_amount_col,self.__bank_amount_col,self.__cash_amount_col]
        row_num = self.__shelf[self.getDate()[1]].get('date_pointer',3)
        while(any([self.__ws[(x+str(row_num))].value for x in data_cols])):
            row_num+=1
        pointer=self.__date_col+str(row_num)
        self.__shelf[self.getDate()[1]]['date_pointer']=row_num
        self.__ws[pointer],_ = self.getDate()
        self.__shelf[self.__current_date]=self.__shelf.get(self.__current_date,{})
        self.__shelf[self.__current_date]['entry_count']=self.__shelf[self.__current_date].get('entry_count',0)
        self.__shelf[self.__current_date]['total_exp']=0
    def get_total_in_col(self,col):
        self.open_workbook()
        pointer=self.__shelf[self.getDate()[1]]['date_pointer']
        till_yesterday= sum([int(self.__ws[col+str(row)].value) for row in range(3,pointer) if (self.__ws[col+str(row)]).value])
        todays=0
        while (self.__ws[col+str(pointer)].value):
            todays+=int(self.__ws[col+str(pointer)].value)
            pointer+=1
        self.close_workbook()
        return till_yesterday+todays

    def do_transfer(self,amount,source,target):
        self.add_log(amount,target,'money moved from '+source)
        self.add_log('-'+amount,source,'money moved to '+target)
        return

    def get_month_total_cash(self):
        return self.get_total_in_col(self.__cash_amount_col)

    def get_month_total_cards(self):
        return self.get_total_in_col(self.__bank_amount_col)

    def get_month_total_wallets(self):
        return self.get_total_in_col(self.__wallet_amount_col)

    def get_asset_value(self):
        return self.get_month_total_cash()+self.get_month_total_cards()+self.get_month_total_wallets()

    def get_all_shelf_items(self):
        self.open_workbook()
        d=dict(self.__shelf)
        self.close_workbook()
        return d

    def get_monthly_limit(self):
        self.open_workbook()
        d=self.__shelf[self.getDate()[1]]['Income']
        self.close_workbook()
        return d



if(__name__=='__main__'):
    lf=LittleFinger()
