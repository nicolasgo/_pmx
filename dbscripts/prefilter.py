#!/usr/bin/python

import re
import sys
import traceback
import config
import datetime
import binascii
import socket

# Regular expressions
#
line_nginx_full_re = re.compile(r"""\[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST|HEAD) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<referer>(\-)|(.*))["]) (["](?P<useragent>.*)["]) (?P<id>\w+)""", re.IGNORECASE)

line_nginx_wifi_re = re.compile(r"""\[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST|HEAD) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<referer>(\-)|(.*))["]) (["](?P<useragent>.*)["])""", re.IGNORECASE)

line_nginx_re = [line_nginx_full_re, line_nginx_wifi_re]

# Filtering
#
# For each method return True if you want to keep the line parsed

def filter_time(time):
    return len(config.time) == 0 or time.hour in config.time 

def filter_msisdn(msisdn):
    return len(config.msisdn) == 0 or msisdn in config.msisdn 

def filter_retcode(retcode):
    return len(config.retcode) == 0 or retcode in config.retcode  

def filter_numbytes(numbytes):
    return True

def filter_ip(ip):
    return len(config.ip) == 0 or ip in config.ip  

def filter_useragent(useragent):
    return len(config.useragent) == 0 or useragent in config.useragent  

def filter_path(path):
    return len(config.path) == 0 or path in config.path  

def filter(time, msisdn, retcode, numbytes, ip, useragent, path):
    return  filter_time(time) and \
            filter_msisdn(msisdn) and \
            filter_retcode(retcode) and \
            filter_numbytes(numbytes) and \
            filter_ip(ip) and \
            filter_useragent(useragent) and \
            filter_path(path)


for file in config.input_files:
    out = open(file+'.pre', 'w')
    with open(file) as f:
        for line in f:
            try :
                first = line.split(' - ')

                ip = first[0].split(' ')[0].strip()

                for regexp in line_nginx_re:
                    match = regexp.search(first[1])
                    if match:
                        dct = match.groupdict()
                        time = datetime.datetime.strptime(dct['dateandtime'].rpartition(' ')[0],  "%d/%b/%Y:%H:%M:%S" )
                        path = dct['url']
                        numbytes = int(dct['bytessent'])
                        msisdn = dct['id']
                        retcode = int(dct['statuscode'])
                        useragent = dct['useragent']

                        if filter(time, msisdn, retcode, numbytes, ip, useragent, path):
                            out.write(line)
                        break;
                    else:
                        sys.stderr.write(' '.join(['No regexp match', line, '\n']))
            
            except :
                print "ERROR:", line
                traceback.print_exc()

    out.close()
