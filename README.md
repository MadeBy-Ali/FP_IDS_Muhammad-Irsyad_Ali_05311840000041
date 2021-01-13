# FP_IDS_Muhammad Irsyad Ali-05311840000041

Penjelasan Ide Project dan program, Sistem Deteksi & Intrusi, 2020  
  * Muhammad Irsyad Ali (05311840000041)  
  
[1. Tahap persiapan](#Tahap-Persiapan)  
[2. Penjelasan](#Penjelasan)  
[a. dnslog.py](#1)  
[b. startdns.py](#2)  
[c. whatsapp.py](#3)    
[3. Dokumentasi](#Dokumentasi)


---
## DNS Logging
---

## tahap-persiapan
* Program ini membutuhkan python 3
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

#### 1
#### dnslog.py
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
* Pada bagian ini didefinisikan nama, tempat lokasi dimana log akan berada, permission dan lain lain. Juga didefinisikan `snap_len` dan `promiscuous_mode` untuk keperluan pcapy
* Kemudian didefinisikan juga `dns_query_lut` yang merupakan jenis jenis DNS record yang akan di capture

##### Fungsi is_corrupted
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
* Fungsi untuk pengecekan file log

##### Fungsi get_log_handle
```bash
def get_log_handle(sec):
    global _log_path
    global _log_handle

    localtime = time.localtime(sec)
    _ = os.path.join(LOG_DIRECTORY, "%d-%02d-%02d.log.gz" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)) 

    if _ != _log_path:
        if os.path.exists(_) and is_corrupted(_):
            i = 1
            while True:
                candidate = _.replace(".log.gz", ".log.%d.gz" % i)
                if not os.path.exists(candidate):
                    shutil.move(_, candidate)
                    break
                else:
                    i += 1

        if not os.path.exists(_):
            open(_, "w+").close()
            os.chmod(_, DEFAULT_LOG_PERMISSIONS)

        _log_path = _
        _log_handle = gzip.open(_log_path, "ab")

    return _log_handle
```
* fungsi ini akan membuat penamaan file log dengan format `%d-%02d-%02d.log.gz" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday`, dimana waktu didapat dari penggunaan
`time.localtime`
* fungsi ini juga akan melakukan pengecekan jika sebelumnya sudah dibuat file yang sama, misalnya dilakukan lebih dari satu logging pada satu hari, maka penamaan akan dirubah 
menggunakan `candidate = _.replace(".log.gz", ".log.%d.gz" % i`. Dengan menggunakan counter (i), maka penamaan file akan menyesuaikan i yang bertambah, seperti 
```bash
2021-01-12.log.gz
2021-01-12.log.1.gz
2021-01-12.log.2.gz
```
* fungsi ini juga akan me return `_log_handle` dimana berisi file log yang sudah dibuka dengan `gzip.open(_log_path, "ab")`

##### Fungsi log_write
```bash
def log_write(sec, text):
    global _counter
    global _flush_last

    _counter += 1

    handle = get_log_handle(sec)

    if CONSOLE_OUTPUT:
        sys.stdout.write(text)
        sys.stdout.flush()

    elif SHOW_COUNTER:
        sys.stdout.write("\r%d" % _counter)
        sys.stdout.flush()

    handle.write(text.encode("utf8") if hasattr(text, "encode") else text)

    if _flush_last is None or (time.time() - _flush_last) >= FLUSH_LOG_TIMEOUT:
        handle.flush()
        _flush_last = time.time()
```
* Fungsi ini akan dipanggil untuk menulisakan kedalam file yang sudah dibuat dengan urutan tertentu dan melakukan flush

##### Fungsi safe_csv_value
```bash
def safe_csv_value(value):
    retval = str(value or '-')
    if any(_ in retval for _ in (' ', '"')):
        retval = "\"%s\"" % retval.replace('"', '""')
    return retval
```

##### Fungsi packet_handler
```bash
def packet_handler(header, packet):
    try:
        if _datalink == pcapy.DLT_LINUX_SLL:
            packet = packet[2:]
        eth = dpkt.ethernet.Ethernet(packet)
        if eth.type == dpkt.ethernet.ETH_TYPE_IP:
            ip = eth.data
            ip_data = ip.data

            src_ip = socket.inet_ntoa(ip.src)   
            dst_ip = socket.inet_ntoa(ip.dst)

            if isinstance(ip_data, dpkt.udp.UDP):
                udp = ip_data
                msg = dpkt.dns.DNS(udp.data)
                sec, usec = header.getts()
                if msg.qd[0].name:
                    query = msg.qd[0].name.lower()
                    parts = query.split('.')
                    answers = []

                    if len(parts) < 2 or parts[-1].isdigit() or ".intranet." in query or any(query.endswith(_) for _ in (".guest", ".in-addr.arpa", ".local")) or re.search(r"\A\d+\.\d+\.\d+\.\d+\.", query) or re.search(r"\d+-\d+-\d+-\d+", parts[0]):  # (e.g. labos, labos.8.8.4.4, 57.8.68.217.checkpoint.com, 2-229-52-28.ip195.fastwebnet.it, dynamic-pppoe-178-141-14-141.kirov.pv.mts.ru)
                        return

                    if udp.sport == 53:
                        for an in msg.an:
                            if hasattr(an, "ip"):
                                answers.append(socket.inet_ntoa(an.ip))

                    if udp.dport == 53:
                        log_write(sec, "%s.%06d Q %s %s %s %s %s\n" % (time.strftime("%H:%M:%S", time.localtime(sec)), usec, DNS_QUERY_LUT[msg.qd[0].type], src_ip, dst_ip, safe_csv_value(query), "?"))
                    if udp.sport == 53:  # and msg.qr == dpkt.dns.DNS_A:
                        log_write(sec, "%s.%06d R %s %s %s %s %s\n" % (time.strftime("%H:%M:%S", time.localtime(sec)), usec, DNS_QUERY_LUT[msg.qd[0].type], src_ip, dst_ip, safe_csv_value(query), safe_csv_value(','.join(answers))))

    except KeyboardInterrupt:
        raise

    except:
        if SHOW_TRACE:
            traceback.print_exc()
```
* Fungsi ini berguna untuk melakukan segala keperluan capture packet yang diawali dengan pendefinisian paket menggunakan `pcapy` dan `dpkt`
* kemudian juga di definisikan `scr ip` dan `dst ip` menggunakan socket
* Kemudian untuk penulisan kedalam file log, digunakan `log_write()` dengan urutan jam/menit/detik, waktu local, usec, DSN record, source ip, destination ip dengan menggunakan
`log_write(sec, "%s.%06d Q %s %s %s %s %s\n" % (time.strftime("%H:%M:%S", time.localtime(sec)), usec, DNS_QUERY_LUT[msg.qd[0].type], src_ip, dst_ip, safe_csv_value(query), "?"))`

##### Fungsi main
```bash
def main():
    global _cap
    global _datalink

    for directory in ((LOG_DIRECTORY,)):
        if not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except:
                exit("[x] not enough permissions to create the directory '%s'. Please rerun with sudo/root privileges" % directory)

    print("[o] log directory '%s'" % LOG_DIRECTORY)

    print("[i] running...")

    try:
        _cap = pcapy.open_live(CAPTURE_INTERFACE, SNAP_LEN, PROMISCUOUS_MODE, CAPTURE_TIMEOUT)
        _cap.setfilter(CAPTURE_FILTER)
        _datalink = _cap.datalink()
        _cap.loop(-1, packet_handler)
    except KeyboardInterrupt:
        print("[!] Ctrl-C pressed")
    except pcapy.PcapError as ex:
        if "permission" in str(ex):
            exit("[x] not enough permissions to capture traffic. Please rerun with sudo/root privileges")
        else:
            raise
```
* pertama fungsi ini akan membuat direktory tersendiri yang menyimpan file log
* kemudian akan dijalankan `pcapy.open_live()` untuk keperluan capture packet dengan waktu dan mode yang sudah ditentukan
* lalu fungsi `packet_handler` dipanggil dan di loop menggunakan `_cap.loop(-1, packet_handler)` yang akan terus berjalan kecuali dilakukan keyboard interupt

##### Main
```bash
if __name__ == "__main__":
    try:
        main()
    except (SystemExit, Exception) as ex:
        print(ex)
    finally:
        if _log_handle:
            try:
                _log_handle.flush()
                _log_handle.close()
            except:
                pass
```

#### 2
#### startdns.py
* startdns.py berfungsi sebagai interface yang digunakan oleh user, disini user bisa menjalankan loggingnya dan menentukan filter apa yang mau digunakan
##### Import
```bash
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
```
* import yang digunakan sama persis dengan `dnslog.py`

##### Fungsi filter query
```bash
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
```
* fungsi ini adalah untuk melakukan filter paacket `query` dari ip yang ditentukan menggunakan `a = os.system(zcat /var/log/dnslog/2018-07-10.log.gz | grep "Q " | grep "ip input")`

##### Fungsi filter response
```bash
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
```
* fungsi ini adalah untuk melakukan filter paacket `Response` dari ip yang ditentukan menggunakan `os.system(zcat /var/log/dnslog/2018-07-10.log.gz | grep "R " | grep "ip input")`

##### Fungsi quick scan
```bash
def quick_scan():
        chc = raw_input("masukin current date untuk latest log, atau custom date dengan format year_mon_day\n")
        os.system("zcat /var/log/dnslog/%d-%d-%d.log.gz" % (chc) | head)

        os.system("source source ./pywhatsapp/bin/activate")
        os.system("python whatsapp.py")
```
* Fungsi ini berguna untuk menampilkan beberapa data teratas dari sebuah file log yang sudah terbuat dengan menggunakan ` os.system("zcat /var/log/dnslog/%d-%d-%d.log.gz" % (chc) | head)`

##### Interface menu & option
```bash
def my_quit_fn():
   raise SystemExit


def invalid():
   print "INVALID CHOICE!"

menu = {"1":("Mulai capture",my_add_fn),"2":("Filter query",filter_satu),"3":("Filter response",filter_dua),"4":("Quick scan",quick_scan),"5":("quit",my_quit_fn),}



for key in sorted(menu.keys()):
     print key+":" + menu[key][0]

ans = raw_input("Make A Choice")
menu.get(ans,[None,invalid])[1]()

```
#### 3
#### whatsapp.py
* whatsapp.py berfungsi untuk mengirimkan notifikasi ke pengguna jika ada filter yang terpenuhi dengan mengirimpan pesan via Whatsapp
```bash
from twilio.rest import Client

client = Client()


from_whatsapp_number='whatsapp:+14155238886'

to_whatsapp_number='whatsapp:+6281808762209'

client.messages.create(body='logging telah dilakukan, terdadpat satu Query/Request yang tidak diinginkan!',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
```

## Dokumentasi

#### Tampilan logging sedang berjalan
![dokum_1](https://github.com/irsyadali1/FP_SDI_05311840000041/blob/main/dokum%20fp%20sdi/tampilan%20logging%20berjalan.png)
#### Contoh tampilan quick capture
![dokum_2](https://github.com/irsyadali1/FP_SDI_05311840000041/blob/main/dokum%20fp%20sdi/contoh%20quick%20capture.png)
#### Contoh filter response dengan ip atau domain tertentu
![dokum_3](https://github.com/irsyadali1/FP_SDI_05311840000041/blob/main/dokum%20fp%20sdi/contoh%20filter%20response%20dengan%20ip%20atau%20domain%20tertentu.png)
#### Contoh query response dengan ip atau domain tertentu
![dokum_4](https://github.com/irsyadali1/FP_SDI_05311840000041/blob/main/dokum%20fp%20sdi/contoh%20filter%20query%20dengan%20ip%20atau%20domain%20tertentu.png)
#### Contoh notifikasi whatsapp
![dokum_5](https://github.com/irsyadali1/FP_SDI_05311840000041/blob/main/dokum%20fp%20sdi/contoh%20notifikasi%20whatsapp.png)


