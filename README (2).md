# 🤖 Bot Shopee Monitor - METODE PALING RELIABLE

Bot Telegram untuk monitoring produk Shopee dengan **3 metode fallback** agar lebih reliable.

## 🎯 Kenapa Versi Ini Lebih Reliable?

| Metode | Kecepatan | Reliability | Fallback |
|--------|-----------|-------------|----------|
| ✅ API v4 | ⚡⚡⚡ Sangat Cepat | ⭐⭐⭐ Sedang | Ya |
| ✅ HTML Scraping | ⚡⚡ Sedang | ⭐⭐⭐⭐⭐ Sangat Reliable | Ya |
| ✅ API v2 | ⚡⚡⚡ Cepat | ⭐⭐ Rendah | - |

**Bot akan otomatis coba 3 metode** sampai berhasil!

## 📱 Instalasi di Termux

### 1. Install Termux

Download dari [F-Droid](https://f-droid.org/packages/com.termux/) (recommended)

### 2. Clone & Setup

```bash
# Install git
pkg install git -y

# Clone repo
git clone https://github.com/CZzRs5dpos/shopee-telegram-notifier.git
cd shopee-telegram-notifier

# Setup otomatis
bash setup.sh
```

### 3. Dapatkan Token Telegram

**A. Buat Bot:**
1. Buka Telegram, cari `@BotFather`
2. Kirim `/newbot`
3. Nama bot: `Shopee Monitor`
4. Username: `shopee_monitor_bot` (harus unique)
5. **COPY TOKEN** yang diberikan

**B. Dapatkan Chat ID:**
1. Cari `@userinfobot` di Telegram
2. Kirim pesan apa saja
3. **COPY Chat ID** yang diberikan

### 4. Konfigurasi

Edit file `.env`:

```bash
nano .env
```

Isi seperti ini (ganti dengan data Anda):

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
CHECK_INTERVAL=300
```

Save: `Ctrl+X` → `Y` → `Enter`

### 5. Tambah Produk

Edit `config.py`:

```bash
nano config.py
```

Cari bagian `PRODUCTS` dan edit:

```python
PRODUCTS = {
    'iPhone 15 Pro': 'https://shopee.co.id/Apple-iPhone-15-Pro-Max-i.74258432.23480203563',
    'Samsung S24': 'https://shopee.co.id/...',
    'Laptop ASUS': 'https://shopee.co.id/...',
}
```

**Cara dapat URL Shopee:**
1. Buka app Shopee
2. Buka produk yang mau dimonitor
3. Klik "Bagikan" / "Share"
4. Copy link
5. Paste ke `config.py`

### 6. Test Dulu!

```bash
python test_bot.py
```

Kalau semua ✅ OK, lanjut ke step 7.

### 7. Jalankan Bot

```bash
python bot_reliable.py
```

Bot akan mulai monitoring! 🎉

## 🔄 Jalankan di Background

### Metode 1: Screen (RECOMMENDED)

```bash
# Install
pkg install screen -y

# Jalankan
screen -S shopee

# Di dalam screen, jalankan bot
python bot_reliable.py

# Detach (bot tetap jalan): Ctrl+A lalu D

# Lihat lagi nanti:
screen -r shopee

# Stop bot: Ctrl+C di dalam screen
```

### Metode 2: nohup

```bash
nohup python bot_reliable.py > output.log 2>&1 &

# Lihat log
tail -f output.log

# Stop
ps aux | grep bot_reliable
kill <PID>
```

## 📊 Contoh Notifikasi

```
🎉✨🛒 PRODUK READY STOCK! 🎉✨🛒

📦 Produk: iPhone 15 Pro Max 256GB

💰 Harga: Rp 18.999.000
📊 Stok: READY ✅
🛒 Terjual: 1234 unit
🏪 Toko: Apple Official Store

🔗 BELI SEKARANG:
https://shopee.co.id/...

🤖 Metode: HTML Scraping (JSON-LD)
⏰ 21-10-2025 12:30:45
```

## 🔧 Troubleshooting

### ❌ "SEMUA METODE GAGAL!"

**Penyebab:**
1. URL produk salah
2. Koneksi internet lemah
3. Shopee maintenance

**Solusi:**
```bash
# Cek URL dulu
python test_bot.py

# Cek internet
ping google.com

# Tunggu 10-30 menit, coba lagi
```

### ❌ Bot tidak kirim pesan

```bash
# Test manual
python test_bot.py

# Pastikan:
# 1. Token benar
# 2. Chat ID benar
# 3. Sudah kirim /start ke bot
```

### ❌ Bot mati saat layar mati

```bash
# Disable battery optimization untuk Termux
# Settings → Apps → Termux → Battery → Unrestricted

# Gunakan screen
screen -S shopee
python bot_reliable.py
# Ctrl+A lalu D
```

### ❌ Error: "No module named 'requests'"

```bash
pip install -r requirements.txt --force-reinstall
```

## 💡 Tips

1. **Interval minimal 300 detik (5 menit)** agar tidak di-ban
2. **Maksimal 5-10 produk** untuk monitoring stabil
3. **Gunakan WiFi** untuk 24/7 monitoring
4. **Backup .env** agar tidak perlu setup ulang
5. **Cek log** di `bot.log` kalau ada masalah

## 📈 Monitoring Multiple Produk

```python
# Di config.py
PRODUCTS = {
    'Produk 1': 'URL_1',
    'Produk 2': 'URL_2',
    'Produk 3': 'URL_3',
    # Maksimal 10 produk recommended
}
```

## 🆘 Masih Gagal?

1. **Screenshot error** yang muncul
2. **Copy isi bot.log**
3. **Buat issue** di GitHub dengan detail error

## 📜 License

MIT License - Bebas digunakan

---

**Dibuat dengan ❤️ untuk pemburu produk ready stock!**

*Note: Gunakan dengan bijak dan patuhi TOS Shopee*