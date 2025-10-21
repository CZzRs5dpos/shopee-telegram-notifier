#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test Bot Telegram dan Shopee Scraping"""

import requests
from config import Config
from bot_reliable import ShopeeMonitorReliable

def test_telegram():
    """Test koneksi Telegram"""
    print("\n" + "="*60)
    print("  TEST KONEKSI TELEGRAM")
    print("="*60 + "\n")
    
    config = Config()
    
    if not config.validate():
        return False
    
    print("1️⃣ Test getMe...")
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot = data['result']
                print(f"   ✅ Bot: @{bot['username']}")
            else:
                print(f"   ❌ Error: {data}")
                return False
        else:
            print(f"   ❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n2️⃣ Test kirim pesan...")
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        message = "🧪 <b>Test Berhasil!</b>\n\nBot siap digunakan! ✅"
        data = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Pesan terkirim!")
        else:
            print(f"   ❌ Gagal: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True


def test_shopee():
    """Test scraping Shopee"""
    print("\n" + "="*60)
    print("  TEST SCRAPING SHOPEE")
    print("="*60 + "\n")
    
    monitor = ShopeeMonitorReliable()
    
    if not monitor.products:
        print("❌ Tidak ada produk di config.py!")
        return False
    
    # Ambil produk pertama untuk test
    product_name, product_url = list(monitor.products.items())[0]
    
    print(f"🔍 Test dengan produk: {product_name}")
    print(f"🔗 URL: {product_url}\n")
    
    product_info = monitor.get_product_info(product_url)
    
    if product_info:
        print("\n✅ BERHASIL AMBIL DATA!")
        print(f"📦 Nama: {product_info['name']}")
        print(f"💰 Harga: Rp {product_info['price']:,.0f}")
        print(f"📊 Status: {'READY ✅' if product_info['is_available'] else 'HABIS ❌'}")
        print(f"🤖 Metode: {product_info['method']}")
        return True
    else:
        print("\n❌ GAGAL AMBIL DATA!")
        print("\nKemungkinan penyebab:")
        print("1. URL produk salah")
        print("2. Koneksi internet bermasalah")
        print("3. Shopee sedang maintenance")
        return False


def main():
    print("\n" + "#"*60)
    print("  BOT SHOPEE MONITOR - TESTING")
    print("#"*60)
    
    # Test Telegram
    telegram_ok = test_telegram()
    
    # Test Shopee
    shopee_ok = test_shopee()
    
    # Summary
    print("\n" + "="*60)
    print("  HASIL TEST")
    print("="*60)
    print(f"Telegram: {'✅ OK' if telegram_ok else '❌ GAGAL'}")
    print(f"Shopee:   {'✅ OK' if shopee_ok else '❌ GAGAL'}")
    print("="*60 + "\n")
    
    if telegram_ok and shopee_ok:
        print("🎉 SEMUA TEST BERHASIL!")
        print("🚀 Bot siap dijalankan: python bot_reliable.py\n")
    else:
        print("⚠️  Ada yang gagal! Perbaiki dulu sebelum jalankan bot.\n")


if __name__ == "__main__":
    main()