# -*- coding: utf8 -*-

import re
from datetime import datetime


def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                    r'(\d+.\d+.\d+.\d+)\s-\s-\s'
                    r'\[(.+)\]\s'
                    r'"GET\s(.+)\s\w+/.+"\s'
                    r'(\d+)\s'
                    r'(\d+)\s'
                    r'"(.+)"\s'
                    r'"(.+)"'
                    )
        parser = re.findall(pattern,logfile.read())
        return parser

def main():
    ip_dict={}
    url_dict={}
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    for log in logs:
        if '11/Jan/2017' in log[1]:
            if log[0] in ip_dict.keys():
                ip_dict[log[0]] += 1
            else:
                ip_dict[log[0]] = 1
    max_ip = ''
    max_number = 0
    for ip in ip_dict.keys():
        if ip_dict[ip]>max_number:
            max_ip = ip
            max_number = ip_dict[ip]
    for log in logs:
        if log[3] == '404':
            if log[2] in url_dict.keys():
                url_dict[log[2]] += 1
            else:
                url_dict[log[2]] = 1
    max_url = ''
    max_number = 0
    for url in url_dict.keys():
        if url_dict[url] > max_number:
            max_url = url
            max_number = url_dict[url]
    return {max_ip:ip_dict[max_ip]},{max_url:url_dict[max_url]}

if __name__ == '__main__':
    ip_dict,url_dict = main()
    print(ip_dict,url_dict)
