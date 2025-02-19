# 🚀 Advanced Port Scanner by ALECS

## 📋 Descriere
Un scanner de porturi avansat și colorat pentru Termux/Android și sisteme Linux/Windows. Creat de ALECS pentru comunitatea de securitate.

## 💻 Repository
- GitHub: [@arian.222](https://github.com/arian.222)
- Project: [Port Scanner](https://github.com/arian.222/port-scanner)

## 🌟 Caracteristici Principale

### 🔍 Scanare Avansată
- Scanare TCP rapidă multi-thread
- Scanare porturi UDP comune
- Detectare automată servicii și versiuni
- Detectare sistem de operare țintă
- Scanare intervale personalizate de porturi

### 🎨 Interfață
- Design colorat și animat
- Indicator de progres în timp real
- Banner personalizat animat
- Text curcubeu pentru mesaje importante
- Emoji-uri pentru o experiență vizuală mai bună

### 📊 Raportare
- Salvare rezultate în format JSON
- Detectare automată servicii
- Timestamp pentru fiecare scanare
- Informații detaliate despre porturi

## 🛠️ Instalare

### Pentru Termux
```bash
# Actualizare pachete
pkg update && pkg upgrade

# Instalare dependințe
pkg install python git

# Clonare repository
git clone https://github.com/arian.222/port-scanner
cd port-scanner

# Permisiuni execuție
chmod +x port_scanner.py
```

### Pentru Linux/Windows
```bash
# Clonare repository
git clone https://github.com/arian.222/port-scanner
cd port-scanner

# Instalare dependințe (dacă este necesar)
pip install -r requirements.txt
```

## 📱 Utilizare

### Comandă de Bază
```bash
python port_scanner.py <ip_address>
```

### Opțiuni Disponibile
```bash
python port_scanner.py <ip_address> [opțiuni]

Opțiuni:
  --udp              : Scanează porturi UDP comune
  --version          : Detectează versiunile serviciilor
  --range start end  : Scanează un interval specific de porturi
  --save filename    : Salvează rezultatele în fișier JSON
  --os              : Detectează sistemul de operare țintă
```

### Exemple de Utilizare
```bash
# Scanare simplă
python port_scanner.py 192.168.1.1

# Scanare completă cu toate opțiunile
python port_scanner.py 192.168.1.1 --udp --version --os --save results.json

# Scanare interval specific
python port_scanner.py 192.168.1.1 --range 80 443

# Scanare website
python port_scanner.py google.com --version
```

## 🎯 Caracteristici Detaliate

### Scanare TCP
- Scanare rapidă multi-thread (100 thread-uri)
- Timeout optimizat (2 secunde per port)
- Primele 1024 porturi scanate implicit
- Detectare servicii pentru porturi deschise

### Scanare UDP
- Verificare porturi UDP comune
- Detectare stare (deschis/închis/filtrat)
- Porturi UDP importante (DNS, DHCP, NTP, etc.)

### Detectare Versiuni
- Banner grabbing pentru servicii
- Detectare versiuni HTTP/HTTPS
- Informații detaliate despre servicii

### Salvare Rezultate
- Format JSON structurat
- Timestamp pentru fiecare scanare
- Informații despre sistemul de operare
- Lista completă de porturi și servicii

## ⚠️ Notă de Securitate
Acest script este destinat doar pentru:
- Testarea sistemelor proprii
- Sisteme pentru care aveți permisiune explicită
- Scopuri educaționale și de cercetare

Scanarea neautorizată a porturilor poate fi ilegală!

## 📞 Contact și Suport

### Creator
ALECS - Expert în Securitate

### Contact
- 💬 Telegram: @alecss12
- 📱 WhatsApp: +40732159658
- 🌐 GitHub: [@arian.222](https://github.com/arian.222)

### Suport
Pentru suport tehnic sau raportare probleme, contactați-mă pe Telegram sau WhatsApp.

## 📄 Licență
Acest proiect este distribuit sub licența MIT.

---
Created with ❤️ by ALECS | GitHub: [@arian.222](https://github.com/arian.222) 