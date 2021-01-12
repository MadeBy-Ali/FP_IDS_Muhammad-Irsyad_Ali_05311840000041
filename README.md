# FP_SDI_05311840000041

Penjelasan Ide Project dan program, Sistem Deteksi & Intrusi, 2020  
  * Muhammad Irsyad Ali (05311840000041)

---
## DNS Logging
---

## Tahap Persiapan
* Program ini membUtuhkan adanya `pcapy` dan `dpkt` sehingga instalasi dapat dilakukan dengan cara  
```bash
apt-get install git python python-pcapy python-dpkt
```
* Kemudian mengkonfigurasi crontab(crontab -e) sebagai berikut
```bash
*/1 * * * * if [ -n "$(ps -ef | grep -v grep | grep 'dnslog.py')" ]; then : ; else python /opt/dnslog/dnslog.py &> /var/log/dnslog.log; fi
```
* Karena adanya penggunaan sandbox dari twilio, maka diperlukan melakukan export untuk id dan token pengguna dari twilio dengan menjalankan
```bash
export TWILIO_ACCOUNT_SID='ACxxxxxxxx'
export TWILIO_AUTH_TOKEN='secret auth tokenxxxx'
```
* Selanjutnya adalah melakukan instalasi virtual environment dengan cara `python3 -m venv pywhatsapp`    
* Kemudian mengaktifkannya `source ./pywhatsapp/bin/activate`

## Penjelasan
Ide Project yang saya buat memiliki 3 bagian program, yaitu `dnslog.py`, `startdns.py` dan `whatsapp.py`

#### A: dnslog.py
* dnslog.py berfungsi sebagai program yang akan melakukan segala aktifitas logging dan penulisan kedalam file yang nantinya akan dapat dapat di filter, berikut penjelasan 
tentang dnslog.py

##### Import
```bash
#!/usr/bin/env python

import gzip 
import io
import os 
import re 
import shutil 
import socket 
import stat 
import sys
import time
import traceback

sys.dont_write_bytecode = True
```
* Tahap import untuk segala keperluan program nantinya, `gzip` berfungsi untuk compress decompress terkait hasil logging yang akan ke dalam file berformat `.gz`
* socket digunakan untuk keperluan terkait ip
* time digunakan untuk keperluan terkait penamaan file log

###### Pendefinisian Variabel
```bash
NAME = "DNSlog"
LOG_DIRECTORY = "/var/log/%s" % NAME.lower()
DEFAULT_LOG_PERMISSIONS = stat.S_IREAD | stat.S_IWRITE | stat.S_IRGRP | stat.S_IROTH
CAPTURE_FILTER = "udp port 53" #untuk dns
SNAP_LEN = 65536   #pcapy
PROMISCUOUS_MODE = True #pcapy
CAPTURE_TIMEOUT = 100  # s
FLUSH_LOG_TIMEOUT = 10
SHOW_TRACE = False
CONSOLE_OUTPUT = False
SHOW_COUNTER = False
DNS_QUERY_LUT = {1:'A', 28:'AAAA', 18:'AFSDB', 42:'APL', 257:'CAA', 60:'CDNSKEY', 59:'CDS', 37:'CERT', 5:'CNAME', 49:'DHCID', 32769:'DLV', 39:'DNAME', 48:'DNSKEY', 43:'DS', 55:'HIP', 45:'IPSECKEY', 25:'KEY', 36:'KX', 29:'LOC', 15:'MX', 35:'NAPTR', 2:'NS', 47:'NSEC', 50:'NSEC3', 51:'NSEC3PARAM', 12:'PTR', 46:'RRSIG', 17:'RP', 24:'SIG', 6:'SOA', 33:'SRV', 44:'SSHFP', 32768:'TA', 249:'TKEY', 52:'TLSA', 250:'TSIG', 16:'TXT', 256:'URI', 255:'*', 252:'AXFR', 251:'IXFR', 41:'OPT', 99:'SPF', 38:'A6'}

_cap = None
_counter = 0
_datalink = None
_log_path = None
_log_handle = None
_flush_last = None
```

##### fungsi is_corrupted
```bash
def is_corrupted(path):
    retval = True

    try:
        with gzip.open(path) as f:
            if f.seekable():
                try:
                    f.seek(0, io.SEEK_END)
                except ValueError:  # Python2
                    while True:
                        _ = f.read(1024)
                        if not _:
                            break

                retval = False
    except:
        pass

    return retval
```

  ![topologi_1](https://github.com/.png)
 
#### B: startdns.py

#### C: whatsapp.py
