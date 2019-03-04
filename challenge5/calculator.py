#!/usr/bin/env python3
import sys
import csv
import getopt
from configparser import ConfigParser
from datetime import datetime
from multiprocessing import Process,Queue

class Config:
    def __init__(self,configfile,cityname):
        self._config = {}
        self._config_context = []
        #with open(configfile) as f:
        #    for line in f.readlines():
        #        items = line.split('=')
        #        self._config_context.append(items[0].strip())
        #        self._config_context.append(items[1].strip())
        configparser = ConfigParser()
        configparser.read(configfile,encoding='UTF-8')
        for my_key in ['JiShuL','JiShuH','YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']:
            value = configparser.get(cityname.upper(),my_key)
            self._config[my_key] = value
        #configparser = ConfigParser()
        #configparser.read(configfile,encoding='UTF-8')

    def get_config(self,config):
        return self._config[config]

class UserData:
    def __init__(self, userdatafile):
        self.userdatafile = userdatafile
        self.userdata = {}
        with open(self.userdatafile) as f:
            data = csv.reader(f)
            for i in data:
                self.userdata[i[0]] = i[1]
    def calculator(self,config):
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
            after_tax = salary_after_tax(float(salary) - float(she_bao))
            tax = float(salary) - float(after_tax) - float(she_bao)
            curtime = str(datetime.now())
            curtime = curtime[0:curtime.index('.')]
            user_info = (user,salary,'{:.2f}'.format(she_bao),'{:.2f}'.format(tax),'{:.2f}'.format(after_tax),curtime)
            self.userdata[user] = user_info
    def dumptofile(self,outputfile):
        with open(outputfile,'w') as f:
            for user,salary in self.userdata.items():
                csv.writer(f).writerow(salary)

def salary_after_tax(salary):
    tax = 0
    try:
        if salary - 5000  < 0:
            tax = 0
        elif (salary - 5000) <= 3000:
            tax = (salary-5000) * 0.03
        elif salary - 5000 <= 12000:
            tax = (salary-5000) * 0.1 -210
        elif salary - 5000 <= 25000:
            tax = (salary-5000) * 0.2 -1410
        elif salary - 5000 <= 35000:
            tax = (salary-5000) * 0.25 - 2660
        elif salary -5000 <= 55000:
            tax = (salary-5000) * 0.3 - 4410
        elif salary -5000 <= 80000:
            tax = (salary-5000) * 0.35 - 7160
        else:
            tax = (salary-5000) * 0.45 - 15160
    except:
        print("Parameter Error")
    salary_new = float(salary) - float(tax)

    return salary_new

def read_salary(q,config_file,userdata_file,cityname):
    print('Process:read_salary is running...')
    config = Config(config_file,cityname)
    userdata = UserData(userdata_file)
    q.put((config,userdata))

def cal_tax(q1,q2):
    print('Process:cal_tax is running...')
    config,userdata = q1.get(block=True,timeout=10)
    userdata.calculator(config)
    q2.put(userdata)

def dump_file(q,outputfile):
    print('Process:dump_file is running...')
    userdata = q.get(block=True,timeout=10)
    userdata.dumptofile(outputfile)

def args_deal(args):
    optlist,_ = getopt.getopt(args,'C:c:d:o:')
    opt_dic = dict(optlist)
    return opt_dic['-C'],opt_dic['-c'],opt_dic['-d'],opt_dic['-o']


if __name__ == '__main__':
    # iconfig_file = sys.argv[sys.argv.index('-c') + 1]
    # userdata_file = sys.argv[sys.argv.index('-d') + 1]
    # output_file = sys.argv[sys.argv.index('-o') + 1]
    city_name,config_file,userdata_file,output_file =('','','','')
    if '-h' in sys.argv or '--help' in sys.argv:
        print('''Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata''')
        exit(1)
    else:
        cityname,config_file,userdata_file,output_file = args_deal(sys.argv[1:])
    queue1 = Queue()
    queue2 = Queue()
    Process(target = read_salary,args=(queue1,config_file,userdata_file,cityname)).start()
    Process(target = cal_tax,args=(queue1,queue2)).start()
    Process(target = dump_file(queue2,output_file)).start()

