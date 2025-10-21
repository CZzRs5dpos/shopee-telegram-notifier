#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Notifikasi Telegram - Shopee Product Monitor
METODE PALING RELIABLE - Multiple Fallback Methods
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import logging
from datetime import datetime
from config import Config
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ShopeeMonitorReliable:
    """Monitor Shopee dengan multiple metode fallback"""
    
    def __init__(self):
        self.config = Config()
        self.telegram_token = self.config.TELEGRAM_BOT_TOKEN
        self.chat_id = self.config.TELEGRAM_CHAT_ID
        self.products = self.config.PRODUCTS
        self.check_interval = self.config.CHECK_INTERVAL
        self.product_status = {}
        
        # User agents untuk rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        ]
    
    def get_random_headers(self):
        """Generate random headers"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    def send_telegram_message(self, message):
        """Kirim pesan ke Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Pesan terkirim ke Telegram")
                return True
            else:
                logger.error(f"❌ Gagal kirim: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Error Telegram: {e}")
            return False
    
    def extract_product_ids(self, url):
        """Extract shop_id dan item_id dari URL"""
        try:
            # Format: https://shopee.co.id/product-name-i.SHOP_ID.ITEM_ID
            if '-i.' in url:
                parts = url.split('-i.')[1].split('?')[0].split('.')
                if len(parts) >= 2:
                    shop_id = parts[0]
                    item_id = parts[1]
                    return shop_id, item_id
            
            # Format alternatif: https://shopee.co.id/shop/SHOP_ID/ITEM_ID
            if '/shop/' in url:
                parts = url.split('/shop/')[1].split('?')[0].split('/')
                if len(parts) >= 2:
                    shop_id = parts[0]
                    item_id = parts[1]
                    return shop_id, item_id
            
            logger.error(f"❌ Format URL tidak dikenali: {url}")
            return None, None
            
        except Exception as e:
            logger.error(f"❌ Error extract ID: {e}")
            return None, None
    
    def method_1_api_v4(self, shop_id, item_id):
        """Metode 1: API v4 Shopee (paling cepat)"""
        try:
            url = f"https://shopee.co.id/api/v4/item/get?itemid={item_id}&shopid={shop_id}"
            headers = self.get_random_headers()
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('error') == 0 or data.get('data'):
                    item = data.get('data', {}) if data.get('data') else data.get('item', {})
                    
                    if item:
                        product_info = {
                            'name': item.get('name', 'Unknown'),
                            'price': item.get('price', 0) / 100000,
                            'price_min': item.get('price_min', 0) / 100000,
                            'price_max': item.get('price_max', 0) / 100000,
                            'stock': item.get('stock', 0),
                            'sold': item.get('sold', item.get('historical_sold', 0)),
                            'shop_name': item.get('shop_name', 'Unknown'),
                            'is_available': item.get('stock', 0) > 0,
                            'method': 'API v4'
                        }
                        logger.info(f"✅ Metode 1 (API v4) berhasil")
                        return product_info
            
            logger.warning("⚠️ Metode 1 gagal, coba metode 2...")
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Metode 1 error: {e}")
            return None
    
    def method_2_html_scraping(self, url):
        """Metode 2: Scraping HTML langsung (paling reliable)"""
        try:
            headers = self.get_random_headers()
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Cari JSON-LD script tag (paling reliable)
                scripts = soup.find_all('script', type='application/ld+json')
                
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        
                        # Cek apakah ada data produk
                        if data.get('@type') == 'Product':
                            offers = data.get('offers', {})
                            
                            # Cek availability
                            availability = offers.get('availability', '')
                            is_available = 'InStock' in availability or 'InStock' in str(offers)
                            
                            product_info = {
                                'name': data.get('name', 'Unknown'),
                                'price': float(offers.get('price', 0)),
                                'price_min': float(offers.get('lowPrice', offers.get('price', 0))),
                                'price_max': float(offers.get('highPrice', offers.get('price', 0))),
                                'stock': 1 if is_available else 0,  # JSON-LD tidak ada exact stock
                                'sold': 0,  # Tidak ada di JSON-LD
                                'shop_name': data.get('brand', {}).get('name', 'Unknown') if isinstance(data.get('brand'), dict) else 'Unknown',
                                'is_available': is_available,
                                'method': 'HTML Scraping (JSON-LD)'
                            }
                            logger.info(f"✅ Metode 2 (HTML Scraping) berhasil")
                            return product_info
                            
                    except json.JSONDecodeError:
                        continue
                
                # Fallback: cari button "Beli Sekarang" atau "Habis"
                page_text = response.text.lower()
                
                # Deteksi ketersediaan dari text
                is_available = False
                if 'habis' in page_text or 'sold out' in page_text or 'stok habis' in page_text:
                    is_available = False
                elif 'beli sekarang' in page_text or 'add to cart' in page_text or 'tambah' in page_text:
                    is_available = True
                
                # Ambil title dari meta tag
                title_tag = soup.find('meta', property='og:title')
                product_name = title_tag['content'] if title_tag else 'Unknown'
                
                # Ambil harga dari meta tag
                price_tag = soup.find('meta', property='product:price:amount')
                price = float(price_tag['content']) if price_tag else 0
                
                product_info = {
                    'name': product_name,
                    'price': price,
                    'price_min': price,
                    'price_max': price,
                    'stock': 1 if is_available else 0,
                    'sold': 0,
                    'shop_name': 'Unknown',
                    'is_available': is_available,
                    'method': 'HTML Scraping (Fallback)'
                }
                
                logger.info(f"✅ Metode 2 (HTML Fallback) berhasil")
                return product_info
            
            logger.warning("⚠️ Metode 2 gagal, coba metode 3...")
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Metode 2 error: {e}")
            return None
    
    def method_3_api_v2(self, shop_id, item_id):
        """Metode 3: API v2 Shopee (backup)"""
        try:
            url = f"https://shopee.co.id/api/v2/item/get?itemid={item_id}&shopid={shop_id}"
            headers = self.get_random_headers()
            headers['Referer'] = f'https://shopee.co.id/'
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('item'):
                    item = data['item']
                    
                    product_info = {
                        'name': item.get('name', 'Unknown'),
                        'price': item.get('price', 0) / 100000,
                        'price_min': item.get('price_min', 0) / 100000,
                        'price_max': item.get('price_max', 0) / 100000,
                        'stock': item.get('stock', 0),
                        'sold': item.get('sold', 0),
                        'shop_name': item.get('shop_name', 'Unknown'),
                        'is_available': item.get('stock', 0) > 0,
                        'method': 'API v2'
                    }
                    logger.info(f"✅ Metode 3 (API v2) berhasil")
                    return product_info
            
            logger.warning("⚠️ Metode 3 gagal")
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Metode 3 error: {e}")
            return None
    
    def get_product_info(self, product_url):
        """Ambil info produk dengan multiple fallback methods"""
        logger.info(f"🔍 Mencoba ambil data produk...")
        
        # Extract IDs dari URL
        shop_id, item_id = self.extract_product_ids(product_url)
        
        # Try Metode 1: API v4
        if shop_id and item_id:
            result = self.method_1_api_v4(shop_id, item_id)
            if result:
                result['url'] = product_url
                return result
            time.sleep(2)
        
        # Try Metode 2: HTML Scraping (PALING RELIABLE)
        result = self.method_2_html_scraping(product_url)
        if result:
            result['url'] = product_url
            return result
        time.sleep(2)
        
        # Try Metode 3: API v2
        if shop_id and item_id:
            result = self.method_3_api_v2(shop_id, item_id)
            if result:
                result['url'] = product_url
                return result
        
        logger.error("❌ SEMUA METODE GAGAL!")
        return None
    
    def format_message(self, product_info, status_change):
        """Format pesan notifikasi"""
        if status_change == 'ready':
            emoji = "🎉✨🛒"
            status_text = "PRODUK READY STOCK!"
        elif status_change == 'sold_out':
            emoji = "😢💔"
            status_text = "Produk Habis"
        else:
            emoji = "ℹ️"
            status_text = "Update Status"
        
        # Format harga
        if product_info['price_min'] != product_info['price_max'] and product_info['price_max'] > 0:
            price_text = f"Rp {product_info['price_min']:,.0f} - Rp {product_info['price_max']:,.0f}"
        else:
            price_text = f"Rp {product_info['price']:,.0f}"
        
        message = f"""
{emoji} <b>{status_text}</b> {emoji}

📦 <b>Produk:</b> {product_info['name']}

💰 <b>Harga:</b> {price_text}
📊 <b>Stok:</b> {'READY ✅' if product_info['is_available'] else 'HABIS ❌'}
🛒 <b>Terjual:</b> {product_info.get('sold', 'N/A')} unit
🏪 <b>Toko:</b> {product_info['shop_name']}

🔗 <b>BELI SEKARANG:</b>
{product_info['url']}

🤖 <i>Metode: {product_info['method']}</i>
⏰ <i>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>
"""
        return message
    
    def check_product(self, product_url, product_name):
        """Cek satu produk"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🔍 Checking: {product_name}")
        logger.info(f"{'='*60}")
        
        product_info = self.get_product_info(product_url)
        
        if product_info is None:
            logger.error(f"❌ Tidak bisa ambil data: {product_name}")
            # Kirim notif error jika gagal terus
            if product_url not in self.product_status:
                self.product_status[product_url] = {'fail_count': 0}
            
            self.product_status[product_url]['fail_count'] = self.product_status[product_url].get('fail_count', 0) + 1
            
            if self.product_status[product_url]['fail_count'] >= 3:
                error_msg = f"⚠️ <b>Warning!</b>\n\nGagal ambil data produk <b>{product_name}</b> sebanyak 3x berturut-turut.\n\nCek URL atau koneksi internet."
                self.send_telegram_message(error_msg)
                self.product_status[product_url]['fail_count'] = 0
            
            return
        
        # Reset fail count
        if product_url in self.product_status:
            self.product_status[product_url]['fail_count'] = 0
        
        # First time check
        if product_url not in self.product_status or 'is_available' not in self.product_status[product_url]:
            self.product_status[product_url] = {
                'is_available': product_info['is_available'],
                'fail_count': 0
            }
            status = 'READY ✅' if product_info['is_available'] else 'HABIS ❌'
            logger.info(f"📝 Status awal: {status}")
            return
        
        # Check status change
        previous_status = self.product_status[product_url]['is_available']
        current_status = product_info['is_available']
        
        if previous_status != current_status:
            if current_status:
                logger.info(f"🎉🎉🎉 {product_name} READY STOCK! 🎉🎉🎉")
                message = self.format_message(product_info, 'ready')
                self.send_telegram_message(message)
            else:
                logger.info(f"😢 {product_name} habis stock")
                message = self.format_message(product_info, 'sold_out')
                self.send_telegram_message(message)
            
            self.product_status[product_url]['is_available'] = current_status
        else:
            status = 'READY ✅' if current_status else 'HABIS ❌'
            logger.info(f"✅ Status tidak berubah: {status}")
    
    def start_monitoring(self):
        """Mulai monitoring"""
        logger.info("="*60)
        logger.info("🚀 BOT NOTIFIKASI SHOPEE DIMULAI!")
        logger.info("="*60)
        
        startup_msg = f"""
🤖 <b>Bot Shopee Monitor Aktif!</b>

📋 Monitoring: {len(self.products)} produk
⏱️ Interval: {self.check_interval} detik
🔄 Multi-method fallback: API v4 → HTML Scraping → API v2

Bot akan kirim notif jika ada perubahan status!
"""
        self.send_telegram_message(startup_msg)
        
        while True:
            try:
                logger.info(f"\n{'#'*60}")
                logger.info(f"🔄 PENGECEKAN BARU - {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
                logger.info(f"{'#'*60}\n")
                
                for product_name, product_url in self.products.items():
                    self.check_product(product_url, product_name)
                    # Random delay antar produk
                    delay = random.randint(3, 7)
                    time.sleep(delay)
                
                logger.info(f"\n✅ Pengecekan selesai. Tunggu {self.check_interval} detik...\n")
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("\n⛔ Bot dihentikan")
                goodbye_msg = "⛔ <b>Bot Shopee Monitor Dihentikan</b>\n\nTerima kasih!"
                self.send_telegram_message(goodbye_msg)
                break
                
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                time.sleep(60)


def main():
    try:
        monitor = ShopeeMonitorReliable()
        monitor.start_monitoring()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()