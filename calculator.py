#!/usr/bin/env python3
import sys

def salary_after_tax(salary):
    tax = 0
    try:
        salary  = int(salary) - 5000 - int(salary)*(0.08 + 0.02 + 0.005 + 0.06)
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
    return salary - tax + 5000

for arg in sys.argv[1:]:
    items = arg.split(':')
    print('{}:{:.2f}'.format(items[0],salary_after_tax(items[1])))
