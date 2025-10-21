#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Konfigurasi bot"""
    
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))
    
    # CONTOH PRODUK - GANTI DENGAN PRODUK YANG ANDA MAU MONITOR
    PRODUCTS = {
        'iPhone 15 Pro': 'https://shopee.co.id/Apple-iPhone-15-Pro-Max-i.74258432.23480203563',
        # Tambahkan produk lain di sini dengan format:
        # 'Nama Produk': 'URL Shopee',
    }
    
    @classmethod
    def validate(cls):
        """Validasi konfigurasi"""
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("❌ TELEGRAM_BOT_TOKEN kosong!")
        
        if not cls.TELEGRAM_CHAT_ID:
            errors.append("❌ TELEGRAM_CHAT_ID kosong!")
        
        if not cls.PRODUCTS:
            errors.append("❌ Tidak ada produk yang dimonitor!")
        
        if errors:
            print("\n" + "="*60)
            print("⚠️  KONFIGURASI BELUM LENGKAP!")
            print("="*60)
            for error in errors:
                print(error)
            print("\nEdit file .env dan isi semua field yang diperlukan!")
            print("="*60 + "\n")
            return False
        
        return True