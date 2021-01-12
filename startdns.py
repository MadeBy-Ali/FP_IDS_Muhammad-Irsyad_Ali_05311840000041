#!/usr/bin/env python

import gzip #compress/decompress
import io #input output
import os #os
import re #regular expression
import shutil #copying/removal
import socket #listen ke particular IP
import stat #path
import sys
import time
import traceback

def my_add_fn():
        execfile('dnslog.py')

def filter_satu():
#       fungsi buat check dari query tertentu
        inpt1 = raw_input("masukan current date untuk latest log, atau custom date dengan format year_mon_day\n")
        inpt2 = raw_input("masukin ip tertentu untuk filter response")

       a = os.system(zcat /var/log/dnslog/2018-07-10.log.gz | grep "Q " | grep "ip yang dimasukin")

       if a == err:
        pass
                else:
                        os.system("source ./pywhatsapp/bin/activate")
                        os.system("python whatsapp.py")

def filter_dua():
#       fungsi buat check dari response tertentu
        inpt1 = raw_input("masukan current date untuk latest log, atau custom date dengan format year_mon_day\n")
        inpt2 = raw_input("masukin ip tertentu untuk filte response")

       a = os.system(zcat /var/log/dnslog/2018-07-10.log.gz | grep "R " | grep "ip input")

       if a == err:
        pass
                else:
                        os.system("source source ./pywhatsapp/bin/activate")
                        os.system("python whatsapp.py")


def quick_scan():
        chc = raw_input("masukin current date untuk latest log, atau custom date dengan format year_mon_day\n")
        os.system("zcat /var/log/dnslog/%d-%d-%d.log.gz" % (chc) | head)

        os.system("source source ./pywhatsapp/bin/activate")
        os.system("python whatsapp.py")


def my_quit_fn():
   raise SystemExit


def invalid():
   print "INVALID CHOICE!"

menu = {"1":("Mulai capture",my_add_fn),"2":("Filter query",filter_satu),"3":("Filter response",filter_dua),"4":("Quick scan",quick_scan),"5":("quit",my_quit_fn),}



for key in sorted(menu.keys()):
     print key+":" + menu[key][0]

ans = raw_input("Make A Choice")
menu.get(ans,[None,invalid])[1]()