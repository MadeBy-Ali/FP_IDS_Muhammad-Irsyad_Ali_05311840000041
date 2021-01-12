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
  ![topologi_1](https://github.com/.png)
 
#### B: startdns.py

#### C: whatsapp.py
