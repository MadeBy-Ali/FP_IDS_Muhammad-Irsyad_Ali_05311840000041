# FP_SDI_05311840000041

Penjelasan Ide Project dan program, Sistem Deteksi & Intrusi, 2020  
  * Muhammad Irsyad Ali (05311840000041)

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

### A: Menginstall 
  ![topologi_1](https://github.com/krisnanda59/Jarkom_Modul5__Lapres_T19/blob/main/dokum%20shift%205/topologi_persiapan.png)
 
### B: Subnetting(CIDR)

### C: Routing

### D: DHCP Relay dan DHCP Server

## Soal
### Nomor 1

### Nomor 2

### Nomor 3
