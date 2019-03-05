from datetime import datetime
import re

def find_404():
    url_dict = {}
    log_file = open('nginx.log')
    for line in log_file.readlines():
        matchLog = re.search(r'[GET|POST|PUT] (.*) HTTP/1.1" 404',line,re.M|re.I)
        if matchLog:
            if matchLog.group(1) in url_dict.keys():
                url_dict[matchLog.group(1)] += 1
            else:
                url_dict[matchLog.group(1)] = 1
    max_url = ''
    max_number = 0
    for url in url_dict.keys():
        if url_dict[url] > max_number:
            max_url = url
            max_number = url_dict[url]
    return {max_url:url_dict[max_url]}
def find_111():
    ip_dict = {}
    log_file = open('nginx.log')
    for line in log_file.readlines():
        matchLog = re.search(r'(\d+\.\d+\.\d+\.\d+) - - \[(.+) \+0800\]',line,re.M|re.I)
        if matchLog:
            log_time = matchLog.group(2)
            dt = datetime.strptime(log_time,'%d/%b/%Y:%H:%M:%S')
            if (dt.year,dt.month,dt.day) == (2017,1,11):
                if matchLog.group(1) in ip_dict.keys():
                    ip_dict[matchLog.group(1)] += 1
                else:
                    ip_dict[matchLog.group(1)] = 1
    max_number = 0
    max_ip = ''
    for ip in ip_dict.keys():
        if ip_dict[ip] > max_number:
            max_ip = ip
            max_number = ip_dict[ip]
    return {max_ip:ip_dict[max_ip]}


if __name__ == '__main__':
    ip_dict = find_111()
    url_dict = find_404()
    print(ip_dict,url_dict)
