#!/bin/bash

echo "=========================================="
echo "  Setup Bot Shopee Monitor - RELIABLE"
echo "=========================================="
echo ""

# Update package
echo "📦 Update packages..."
pkg update -y

# Install Python
echo "🐍 Install Python..."
pkg install python -y

# Install Git
echo "📥 Install Git..."
pkg install git -y

# Install dependencies
echo "📚 Install dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ File .env dibuat!"
    echo ""
    echo "⚠️  PENTING! Edit file .env:"
    echo "   nano .env"
else
    echo "✅ File .env sudah ada"
fi

chmod +x bot_reliable.py

echo ""
echo "=========================================="
echo "  ✅ SETUP SELESAI!"
echo "=========================================="
echo ""
echo "📝 Langkah selanjutnya:"
echo "1. Edit .env: nano .env"
echo "2. Edit config.py untuk tambah produk"
echo "3. Test dulu: python test_bot.py"
echo "4. Jalankan bot: python bot_reliable.py"
echo ""