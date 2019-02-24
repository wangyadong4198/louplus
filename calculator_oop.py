#!/usr/bin/env python3
import sys
import csv
class Config:
    def __init__(self,configfile):
        self._config = {}
        self._config_context = []
        with open(configfile) as f:
            for line in f.readlines():
                items = line.split('=')
                self._config_context.append(items[0].strip())
                self._config_context.append(items[1].strip())
            for my_key in ['JiShuL','JiShuH','YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']:
                value = self._config_context[self._config_context.index(my_key) + 1]
                self._config[my_key] = value
    def get_config(self,config):
        return self._config[config]

class UserData:
    def __init__(self, userdatafile):
        self.userdatafile = userdatafile
        self.userdata = {}
        print(self.userdatafile)
        with open(self.userdatafile) as f:
            data = csv.reader(f)
            for i in data:
                self.userdata[i[0]] = i[1]
               # print(i)
        # print('---init---')
        # print(self.userdata)
    def calculator(self):
        after_tax = 0
        she_bao = 0
        tax = 0
     
        for user,salary in self.userdata.items():
            salary_real = salary
            if float(salary) < float(config.get_config('JiShuL')):
                salary_real = float(config.get_config('JiShuL'))
            if float(salary) > float(config.get_config('JiShuH')):
                salary_real = config.get_config('JiShuH')
            she_bao = float(salary_real) * (float(config.get_config('YangLao')) + float(config.get_config('YiLiao')) + float(config.get_config('ShiYe')) + float(config.get_config('GongShang')) + float(config.get_config('ShengYu')) + float(config.get_config('GongJiJin')))
           #  print('shebao{}'.format(she_bao))
            after_tax = salary_after_tax(float(salary) - float(she_bao))
            # print('after_tax{}'.format(after_tax))
            tax = float(salary) - float(after_tax) - float(she_bao)
            user_info = (user,salary,'{:.2f}'.format(she_bao),'{:.2f}'.format(tax),'{:.2f}'.format(after_tax))
            # print(user_info)
            self.userdata[user] = user_info
    def dumptofile(self,outputfile):
        print('-----dump to file------')
        with open(outputfile,'w') as f:
            for user,salary in self.userdata.items():
                print (salary)
                csv.writer(f).writerow(salary)

def salary_after_tax(salary):
    tax = 0
    try:
        if salary < 0:
            tax = 0
        elif salary <= 3000:
            tax = salary * 0.03
        elif salary <= 12000:
            tax = salary * 0.1 -210
        elif salary <= 25000:
            tax = salary * 0.2 -1410
        elif salary <= 35000:
            tax = salary * 0.25 - 2660
        elif salary <= 55000:
            tax = salary * 0.3 - 4410
        elif salary <= 80000:
            tax = salary * 0.35 - 7160
        else:
            tax = salary * 0.45 - 15160
    except:
        print("Parameter Error")
    return int(salary) - float(tax)

if __name__ == '__main__':
    config_file = sys.argv[sys.argv.index('-c') + 1]
    config = Config(config_file)

    userdata_file = sys.argv[sys.argv.index('-d') + 1]
    userdata = UserData(userdata_file)
    
    outputfile = sys.argv[sys.argv.index('-o') + 1]
    userdata.calculator()
    userdata.dumptofile(outputfile)
