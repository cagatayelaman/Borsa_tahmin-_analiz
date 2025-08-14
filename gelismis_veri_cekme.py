#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gelişmiş Canlı Finansal Veri Çekme Araçları
Geliştiren : Çağatay Elaman
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import time
import yfinance as yf
import warnings
import os
warnings.filterwarnings('ignore')

class GelismisVeriCekici:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Türk hisse senetleri için doğru semboller
        self.turk_hisseleri = {
            'THYAO': 'THYAO.IS',      # Türk Hava Yolları
            'GARAN': 'GARAN.IS',      # Garanti Bankası
            'AKBNK': 'AKBNK.IS',      # Akbank
            'ISCTR': 'ISCTR.IS',      # İş Bankası
            'ASELSAN': 'ASELSAN.IS',  # Aselsan
            'KRDMD': 'KRDMD.IS',      # Kardemir
            'SASA': 'SASA.IS',        # Sasa
            'BIMAS': 'BIMAS.IS',      # BİM
            'MGROS': 'MGROS.IS',      # Migros
            'PGSUS': 'PGSUS.IS',      # P&G
            'AEFES': 'AEFES.IS',      # Anadolu Efes
            'KCHOL': 'KCHOL.IS',      # Koç Holding
            'SAHOL': 'SAHOL.IS',      # Sabancı Holding
            'TUPRS': 'TUPRS.IS',      # Tüpraş
            'EREGL': 'EREGL.IS'       # Ereğli Demir Çelik
        }
        
        # Klasör yapısını oluştur
        self.setup_folders()
    
    def setup_folders(self):
        """Klasör yapısını oluştur"""
        # Ana klasörler
        self.folders = {
            'base': 'Finansal_Veriler',
            'detayli': 'Detayli_Veriler',
            'teknik': 'Teknik_Analiz',
            'karsilastirma': 'Karsilastirmalar',
            'tum_veriler': 'Tum_Veriler',
            'manuel': 'Manuel_Veriler',
            'canli': 'Canli_Veriler'
        }
        
        # Bugünün tarihi
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Ana klasörü oluştur
        base_folder = self.folders['base']
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
            print(f"📁 Ana klasör oluşturuldu: {base_folder}")
        
        # Alt klasörleri oluştur
        for folder_name, folder_path in self.folders.items():
            if folder_name != 'base':
                full_path = os.path.join(base_folder, folder_path)
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    print(f"📁 Alt klasör oluşturuldu: {full_path}")
                
                # Tarih klasörü oluştur
                date_path = os.path.join(full_path, today)
                if not os.path.exists(date_path):
                    os.makedirs(date_path)
                    print(f"📁 Tarih klasörü oluşturuldu: {date_path}")
    
    def get_file_path(self, file_type, filename):
        """Dosya türüne göre klasör yolu oluştur"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if file_type == 'detayli':
            folder = os.path.join(self.folders['base'], self.folders['detayli'], today)
        elif file_type == 'teknik':
            folder = os.path.join(self.folders['base'], self.folders['teknik'], today)
        elif file_type == 'karsilastirma':
            folder = os.path.join(self.folders['base'], self.folders['karsilastirma'], today)
        elif file_type == 'tum_veriler':
            folder = os.path.join(self.folders['base'], self.folders['tum_veriler'], today)
        elif file_type == 'manuel':
            folder = os.path.join(self.folders['base'], self.folders['manuel'], today)
        elif file_type == 'canli':
            folder = os.path.join(self.folders['base'], self.folders['canli'], today)
        else:
            folder = os.path.join(self.folders['base'], today)
        
        return os.path.join(folder, filename)
    
    def print_separator(self, title):
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def method1_yfinance_detayli(self, symbol="THYAO.IS", period="1mo"):
        """Yahoo Finance API ile detaylı veri çekme"""
        self.print_separator("YAHOO FINANCE API - DETAYLI VERİ")
        
        try:
            print(f"📊 {symbol} için detaylı veri çekiliyor...")
            print(f"📅 Veri aralığı: {period}")
            
            # Hisse senedi bilgilerini al
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            print(f"🏢 Şirket: {info.get('longName', 'Bilinmiyor')}")
            print(f"💱 Sembol: {symbol}")
            print(f"💰 Mevcut Fiyat: {info.get('currentPrice', 'Bilinmiyor')} TL")
            print(f"📈 Günlük Değişim: {info.get('regularMarketChangePercent', 'Bilinmiyor')}%")
            print(f"📊 Piyasa Değeri: {info.get('marketCap', 'Bilinmiyor')}")
            print(f"📈 52 Hafta Yüksek: {info.get('fiftyTwoWeekHigh', 'Bilinmiyor')}")
            print(f"📉 52 Hafta Düşük: {info.get('fiftyTwoWeekLow', 'Bilinmiyor')}")
            
            # Tarihsel verileri al
            print(f"\n📊 Tarihsel veriler alınıyor...")
            hist = ticker.history(period=period)
            
            if len(hist) > 0:
                print(f"✅ Veri alındı! Toplam {len(hist)} gün")
                print(f"📅 Veri aralığı: {hist.index[0].strftime('%Y-%m-%d')} - {hist.index[-1].strftime('%Y-%m-%d')}")
                
                # Son 10 günün verilerini göster
                print(f"\n📋 Son 10 günün verileri:")
                print(hist.tail(10)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2))
                
                # İstatistikler
                print(f"\n📊 İstatistikler:")
                print(f"   Ortalama Kapanış: {hist['Close'].mean():.2f} TL")
                print(f"   En Yüksek: {hist['High'].max():.2f} TL")
                print(f"   En Düşük: {hist['Low'].min():.2f} TL")
                print(f"   Toplam Hacim: {hist['Volume'].sum():,}")
                
                # Excel olarak kaydet (klasörleme sistemi ile)
                filename = f"{symbol.replace('.IS', '')}_detayli_veri_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                file_path = self.get_file_path('detayli', filename)
                
                # Timezone-aware index'i timezone-naive yap
                hist_clean = hist.copy()
                hist_clean.index = hist_clean.index.tz_localize(None)
                
                hist_clean.to_excel(file_path)
                print(f"\n💾 Veriler kaydedildi: {file_path}")
                
                return hist
            else:
                print("❌ Veri bulunamadı!")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method2_turk_hisseleri_listesi(self):
        """Türk hisse senetleri listesini göster"""
        self.print_separator("TÜRK HİSSE SENETLERİ LİSTESİ")
        
        print("🇹🇷 Borsa İstanbul'da işlem gören popüler hisse senetleri:")
        print()
        
        for kod, sembol in self.turk_hisseleri.items():
            print(f"📈 {kod:8} → {sembol}")
        
        print(f"\n💡 Toplam {len(self.turk_hisseleri)} hisse senedi")
        print("💡 Sembol kullanırken .IS eklemeyi unutmayın!")
        
        # Klasör yapısını göster
        print(f"\n📁 Klasör Yapısı:")
        base_folder = self.folders['base']
        print(f"   📂 Ana Klasör: {base_folder}")
        for folder_name, folder_path in self.folders.items():
            if folder_name != 'base':
                full_path = os.path.join(base_folder, folder_path, datetime.now().strftime('%Y-%m-%d'))
                print(f"   📁 {folder_name.title()}: {full_path}")
        
        return self.turk_hisseleri
    
    def method3_veri_karsilastirma(self, symbol1="THYAO.IS", symbol2="GARAN.IS", period="1mo"):
        """İki hisse senedini karşılaştır"""
        self.print_separator("HİSSE SENEDİ KARŞILAŞTIRMA")
        
        try:
            print(f"📊 {symbol1} vs {symbol2} karşılaştırılıyor...")
            print(f"📅 Veri aralığı: {period}")
            
            # Her iki hisse için veri al
            ticker1 = yf.Ticker(symbol1)
            ticker2 = yf.Ticker(symbol2)
            
            hist1 = ticker1.history(period=period)
            hist2 = ticker2.history(period=period)
            
            if len(hist1) > 0 and len(hist2) > 0:
                print(f"\n✅ Her iki hisse için veri alındı!")
                
                # Son kapanış fiyatları
                son_fiyat1 = hist1['Close'].iloc[-1]
                son_fiyat2 = hist2['Close'].iloc[-1]
                
                # Değişim yüzdeleri
                degisim1 = ((hist1['Close'].iloc[-1] - hist1['Close'].iloc[0]) / hist1['Close'].iloc[0]) * 100
                degisim2 = ((hist2['Close'].iloc[-1] - hist2['Close'].iloc[0]) / hist2['Close'].iloc[0]) * 100
                
                print(f"\n📊 Karşılaştırma Sonuçları:")
                print(f"   {symbol1}: {son_fiyat1:.2f} TL ({degisim1:+.2f}%)")
                print(f"   {symbol2}: {son_fiyat2:.2f} TL ({degisim2:+.2f}%)")
                
                # Performans karşılaştırması
                if degisim1 > degisim2:
                    print(f"\n🏆 {symbol1} daha iyi performans gösterdi!")
                elif degisim2 > degisim1:
                    print(f"\n🏆 {symbol2} daha iyi performans gösterdi!")
                else:
                    print(f"\n🤝 Her iki hisse aynı performansı gösterdi!")
                
                # Excel olarak kaydet (klasörleme sistemi ile)
                filename = f"karsilastirma_{symbol1.replace('.IS', '')}_{symbol2.replace('.IS', '')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                file_path = self.get_file_path('karsilastirma', filename)
                
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Timezone sorunu çözüldü
                    hist1_clean = hist1.copy()
                    hist1_clean.index = hist1_clean.index.tz_localize(None)
                    hist2_clean = hist2.copy()
                    hist2_clean.index = hist2_clean.index.tz_localize(None)
                    
                    hist1_clean.to_excel(writer, sheet_name=f"{symbol1.replace('.IS', '')}")
                    hist2_clean.to_excel(writer, sheet_name=f"{symbol2.replace('.IS', '')}")
                    
                    # Karşılaştırma özeti
                    karsilastirma_df = pd.DataFrame({
                        'Hisse': [symbol1, symbol2],
                        'Son_Fiyat': [son_fiyat1, son_fiyat2],
                        'Degisim_Yuzde': [degisim1, degisim2],
                        'Ortalama_Fiyat': [hist1['Close'].mean(), hist2['Close'].mean()],
                        'En_Yuksek': [hist1['High'].max(), hist2['High'].max()],
                        'En_Dusuk': [hist1['Low'].min(), hist2['Low'].min()]
                    })
                    karsilastirma_df.to_excel(writer, sheet_name='Karsilastirma_Ozeti', index=False)
                
                print(f"\n💾 Karşılaştırma kaydedildi: {file_path}")
                
                return {'hist1': hist1, 'hist2': hist2, 'karsilastirma': karsilastirma_df}
            else:
                print("❌ Veri alınamadı!")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method4_teknik_analiz(self, symbol="THYAO.IS", period="3mo"):
        """Teknik analiz verileri"""
        self.print_separator("TEKNİK ANALİZ")
        
        try:
            print(f"📊 {symbol} için teknik analiz yapılıyor...")
            print(f"📅 Veri aralığı: {period}")
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if len(hist) > 0:
                # Basit teknik göstergeler
                close_prices = hist['Close']
                
                # Hareketli ortalamalar
                ma20 = close_prices.rolling(window=20).mean()
                ma50 = close_prices.rolling(window=50).mean()
                
                # RSI hesaplama (basit)
                delta = close_prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                # Bollinger Bands
                ma20_std = close_prices.rolling(window=20).std()
                upper_band = ma20 + (ma20_std * 2)
                lower_band = ma20 - (ma20_std * 2)
                
                print(f"\n📊 Teknik Analiz Sonuçları:")
                print(f"   Son Fiyat: {close_prices.iloc[-1]:.2f} TL")
                print(f"   20 Günlük MA: {ma20.iloc[-1]:.2f} TL")
                print(f"   50 Günlük MA: {ma50.iloc[-1]:.2f} TL")
                print(f"   RSI: {rsi.iloc[-1]:.2f}")
                print(f"   Bollinger Üst: {upper_band.iloc[-1]:.2f} TL")
                print(f"   Bollinger Alt: {lower_band.iloc[-1]:.2f} TL")
                
                # Sinyal analizi
                current_price = close_prices.iloc[-1]
                ma20_current = ma20.iloc[-1]
                ma50_current = ma50.iloc[-1]
                rsi_current = rsi.iloc[-1]
                
                print(f"\n🎯 Sinyal Analizi:")
                if current_price > ma20_current:
                    print("   ✅ Fiyat 20 günlük ortalamanın üstünde (Pozitif)")
                else:
                    print("   ❌ Fiyat 20 günlük ortalamanın altında (Negatif)")
                
                if ma20_current > ma50_current:
                    print("   ✅ 20 günlük MA, 50 günlük MA'nın üstünde (Yükseliş trendi)")
                else:
                    print("   ❌ 20 günlük MA, 50 günlük MA'nın altında (Düşüş trendi)")
                
                if rsi_current > 70:
                    print("   ⚠️  RSI > 70 (Aşırı alım bölgesi)")
                elif rsi_current < 30:
                    print("   ⚠️  RSI < 30 (Aşırı satım bölgesi)")
                else:
                    print("   ✅ RSI normal bölgede")
                
                # Excel olarak kaydet (klasörleme sistemi ile)
                filename = f"{symbol.replace('.IS', '')}_teknik_analiz_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                file_path = self.get_file_path('teknik', filename)
                
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Ana veri (timezone sorunu çözüldü)
                    hist_clean = hist.copy()
                    hist_clean.index = hist_clean.index.tz_localize(None)
                    hist_clean.to_excel(writer, sheet_name='Ana_Veri')
                    
                    # Teknik göstergeler
                    teknik_df = pd.DataFrame({
                        'Tarih': hist_clean.index,
                        'Kapanis': close_prices,
                        'MA20': ma20,
                        'MA50': ma50,
                        'RSI': rsi,
                        'Bollinger_Ust': upper_band,
                        'Bollinger_Alt': lower_band
                    })
                    teknik_df.to_excel(writer, sheet_name='Teknik_Gostergeler', index=False)
                
                print(f"\n💾 Teknik analiz kaydedildi: {file_path}")
                
                return hist
            else:
                print("❌ Veri bulunamadı!")
                return None
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method5_klasor_yapisi_goster(self):
        """Klasör yapısını göster"""
        self.print_separator("KLASÖR YAPISI")
        
        base_folder = self.folders['base']
        today = datetime.now().strftime('%Y-%m-%d')
        
        print(f"📂 Ana Klasör: {base_folder}")
        print(f"📅 Tarih: {today}")
        print()
        
        print("📁 Alt Klasörler:")
        for folder_name, folder_path in self.folders.items():
            if folder_name != 'base':
                full_path = os.path.join(base_folder, folder_path, today)
                print(f"   📂 {folder_name.title()}: {full_path}")
                
                # Klasördeki dosya sayısını göster
                if os.path.exists(full_path):
                    files = [f for f in os.listdir(full_path) if f.endswith('.xlsx')]
                    print(f"      📄 {len(files)} Excel dosyası")
        
        print(f"\n💡 Toplam Excel dosyası sayısı: {self.count_total_excel_files()}")
    
    def count_total_excel_files(self):
        """Toplam Excel dosyası sayısını hesapla"""
        total = 0
        base_folder = self.folders['base']
        today = datetime.now().strftime('%Y-%m-%d')
        
        for folder_name, folder_path in self.folders.items():
            if folder_name != 'base':
                full_path = os.path.join(base_folder, folder_path, today)
                if os.path.exists(full_path):
                    files = [f for f in os.listdir(full_path) if f.endswith('.xlsx')]
                    total += len(files)
        
        return total
    
    def run_menu(self):
        """Ana menü"""
        self.print_separator("GELİŞMİŞ CANLI VERİ ÇEKME ARAÇLARI")
        
        print("🔧 Mevcut yöntemler:")
        print("1. 📊 Detaylı Yahoo Finance Veri Çekme")
        print("2. 🇹🇷 Türk Hisse Senetleri Listesi")
        print("3. ⚖️  Hisse Senedi Karşılaştırma")
        print("4. 📈 Teknik Analiz")
        print("5. 🚀 TÜM YÖNTEMLERİ OTOMATİK ÇALIŞTIR")
        print("6. 📁 Klasör Yapısını Göster")
        
        while True:
            try:
                choice = input("\n🎯 Hangi yöntemi kullanmak istiyorsunuz? (1-6, q=çıkış): ")
                
                if choice.lower() == 'q':
                    print("👋 Program sonlandırılıyor...")
                    break
                
                elif choice == '1':
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "1mo"
                    self.method1_yfinance_detayli(symbol, period)
                
                elif choice == '2':
                    self.method2_turk_hisseleri_listesi()
                
                elif choice == '3':
                    symbol1 = input("📈 1. Hisse senedi (örn: THYAO.IS): ") or "THYAO.IS"
                    symbol2 = input("📈 2. Hisse senedi (örn: GARAN.IS): ") or "GARAN.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "1mo"
                    self.method3_veri_karsilastirma(symbol1, symbol2, period)
                
                elif choice == '4':
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "3mo"
                    self.method4_teknik_analiz(symbol, period)
                
                elif choice == '5':
                    print("\n🚀 TÜM YÖNTEMLER OTOMATİK ÇALIŞTIRILIYOR!")
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "1mo"
                    
                    print(f"\n📊 {symbol} için tüm analizler yapılıyor...")
                    
                    # Detaylı veri
                    self.method1_yfinance_detayli(symbol, period)
                    
                    # Teknik analiz
                    self.method4_teknik_analiz(symbol, period)
                    
                    print(f"\n🎉 Tüm analizler tamamlandı!")
                
                elif choice == '6':
                    self.method5_klasor_yapisi_goster()
                
                else:
                    print("❌ Geçersiz seçim! 1-6 arası bir sayı girin.")
                
            except KeyboardInterrupt:
                print("\n👋 Program sonlandırılıyor...")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    print("🚀 Gelişmiş Canlı Finansal Veri Çekme Araçları Başlatılıyor...")
    
    # Gerekli kütüphaneleri kontrol et
    try:
        import yfinance
        print("✅ yfinance kütüphanesi mevcut")
    except ImportError:
        print("❌ yfinance kütüphanesi eksik!")
        print("💡 Kurulum: pip install yfinance")
        exit()
    
    print()
    
    # Programı başlat
    veri_cekici = GelismisVeriCekici()
    veri_cekici.run_menu()
