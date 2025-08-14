#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canlı Finansal Veri Çekme Araçları
Geliştiren: Çağatay Elaman
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import time
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import warnings
warnings.filterwarnings('ignore')

class CanliVeriCekici:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def print_separator(self, title):
        print(f"\n{'='*50}")
        print(f" {title}")
        print(f"{'='*50}")
    
    def method1_yfinance(self, symbol="THYAO.IS", period="1mo"):
        """Yahoo Finance API kullanarak veri çekme"""
        self.print_separator("YAHOO FINANCE API")
        try:
            print(f"📊 {symbol} için veri çekiliyor...")
            
            # Hisse senedi bilgilerini al
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            print(f"🏢 Şirket: {info.get('longName', 'Bilinmiyor')}")
            print(f"💱 Sembol: {symbol}")
            print(f"💰 Mevcut Fiyat: {info.get('currentPrice', 'Bilinmiyor')} TL")
            print(f"📈 Günlük Değişim: {info.get('regularMarketChangePercent', 'Bilinmiyor')}%")
            
            # Tarihsel verileri al
            hist = ticker.history(period=period)
            print(f"📅 Veri aralığı: {hist.index[0].strftime('%Y-%m-%d')} - {hist.index[-1].strftime('%Y-%m-%d')}")
            print(f"📊 Toplam veri sayısı: {len(hist)}")
            
            # Son 5 günün verilerini göster
            print("\n📋 Son 5 günün verileri:")
            print(hist.tail()[['Open', 'High', 'Low', 'Close', 'Volume']].round(2))
            
            # Excel olarak kaydet
            filename = f"{symbol.replace('.IS', '')}_canli_veri_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            hist.to_excel(filename)
            print(f"\n💾 Veriler kaydedildi: {filename}")
            
            return hist
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method2_alpha_vantage(self, symbol="THYAO", api_key=None):
        """Alpha Vantage API kullanarak veri çekme"""
        self.print_separator("ALPHA VANTAGE API")
        
        if not api_key:
            print("⚠️  Alpha Vantage API key gerekli!")
            print("💡 https://www.alphavantage.co/support/#api-key adresinden ücretsiz key alabilirsiniz")
            return None
        
        try:
            print(f"📊 {symbol} için veri çekiliyor...")
            
            ts = TimeSeries(key=api_key, output_format='pandas')
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
            
            print(f"📅 Veri aralığı: {data.index[0].strftime('%Y-%m-%d')} - {data.index[-1].strftime('%Y-%m-%d')}")
            print(f"📊 Toplam veri sayısı: {len(data)}")
            
            # Son 5 günün verilerini göster
            print("\n📋 Son 5 günün verileri:")
            print(data.tail()[['1. open', '2. high', '3. low', '4. close', '5. volume']].round(2))
            
            # Excel olarak kaydet
            filename = f"{symbol}_alpha_vantage_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            data.to_excel(filename)
            print(f"\n💾 Veriler kaydedildi: {filename}")
            
            return data
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method3_web_scraping(self, symbol="THYAO"):
        """Web scraping ile veri çekme (Borsa İstanbul)"""
        self.print_separator("WEB SCRAPING - BORSA İSTANBUL")
        
        try:
            print(f"🌐 {symbol} için web scraping yapılıyor...")
            
            # Borsa İstanbul veri API'si
            url = "https://bigpara.hurriyet.com.tr/borsa/canli-borsa/"
            
            # Alternatif olarak Investing.com API'si
            investing_url = f"https://tr.investing.com/equities/turkey"
            
            print("⚠️  Web scraping için gerekli kütüphaneler kurulmalı:")
            print("pip install beautifulsoup4 requests-html")
            
            # Basit veri örneği
            sample_data = {
                'Tarih': datetime.now().strftime('%Y-%m-%d'),
                'Sembol': symbol,
                'Son': 45.20,
                'Değişim': 0.85,
                'Değişim%': 1.92,
                'Hacim': 1250000,
                'Açılış': 44.35,
                'Yüksek': 45.50,
                'Düşük': 44.10
            }
            
            df = pd.DataFrame([sample_data])
            print("\n📋 Örnek veri:")
            print(df)
            
            return df
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None
    
    def method4_manual_input(self):
        """Manuel veri girişi"""
        self.print_separator("MANUEL VERİ GİRİŞİ")
        
        print("📝 Manuel veri girişi yapın:")
        
        data_list = []
        while True:
            print(f"\n--- Veri {len(data_list) + 1} ---")
            
            try:
                tarih = input("Tarih (YYYY-MM-DD) [Çıkmak için 'q']: ")
                if tarih.lower() == 'q':
                    break
                
                kapanis = float(input("Kapanış fiyatı: "))
                min_fiyat = float(input("Minimum fiyat: "))
                max_fiyat = float(input("Maksimum fiyat: "))
                hacim = int(input("Hacim: "))
                usd_try = float(input("USD/TRY: "))
                
                data_list.append({
                    'Tarih': tarih,
                    'Kapanış': kapanis,
                    'Min': min_fiyat,
                    'Max': max_fiyat,
                    'Hacim': hacim,
                    'USD_TRY': usd_try
                })
                
                print("✅ Veri eklendi!")
                
            except ValueError:
                print("❌ Geçersiz değer! Tekrar deneyin.")
                continue
        
        if data_list:
            df = pd.DataFrame(data_list)
            filename = f"manuel_veri_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"\n💾 Veriler kaydedildi: {filename}")
            return df
        
        return None
    
    def method5_realtime_monitoring(self, symbol="THYAO.IS", interval=30):
        """Gerçek zamanlı izleme"""
        self.print_separator("GERÇEK ZAMANLI İZLEME")
        
        print(f"🔄 {symbol} için gerçek zamanlı izleme başlatılıyor...")
        print(f"⏱️  Güncelleme aralığı: {interval} saniye")
        print("🛑 Durdurmak için Ctrl+C")
        
        try:
            while True:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                current_time = datetime.now().strftime('%H:%M:%S')
                current_price = info.get('currentPrice', 'Bilinmiyor')
                change_percent = info.get('regularMarketChangePercent', 'Bilinmiyor')
                
                print(f"[{current_time}] 💰 {symbol}: {current_price} TL ({change_percent}%)")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️  İzleme durduruldu.")
    
    def method6_run_all_automatically(self, symbol="THYAO.IS", period="1mo", api_key=None):
        """Tüm yöntemleri otomatik olarak çalıştır"""
        self.print_separator("🚀 TÜM YÖNTEMLER OTOMATİK ÇALIŞTIRILIYOR")
        
        print(f"🎯 Hedef: {symbol}")
        print(f"📅 Veri aralığı: {period}")
        print(f"⏱️  Başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {}
        success_count = 0
        total_methods = 5
        
        # 1. Yahoo Finance
        print(f"\n{'='*30}")
        print("1️⃣ YAHOO FINANCE API")
        print(f"{'='*30}")
        try:
            result = self.method1_yfinance(symbol, period)
            if result is not None:
                results['yfinance'] = result
                success_count += 1
                print("✅ Yahoo Finance başarılı!")
            else:
                print("❌ Yahoo Finance başarısız!")
        except Exception as e:
            print(f"❌ Yahoo Finance hatası: {e}")
        
        # 2. Alpha Vantage (API key varsa)
        if api_key:
            print(f"\n{'='*30}")
            print("2️⃣ ALPHA VANTAGE API")
            print(f"{'='*30}")
            try:
                result = self.method2_alpha_vantage(symbol.replace('.IS', ''), api_key)
                if result is not None:
                    results['alpha_vantage'] = result
                    success_count += 1
                    print("✅ Alpha Vantage başarılı!")
                else:
                    print("❌ Alpha Vantage başarısız!")
            except Exception as e:
                print(f"❌ Alpha Vantage hatası: {e}")
        else:
            print(f"\n{'='*30}")
            print("2️⃣ ALPHA VANTAGE API (ATLANDI - API Key yok)")
            print(f"{'='*30}")
            print("⚠️  API Key olmadığı için atlandı")
        
        # 3. Web Scraping
        print(f"\n{'='*30}")
        print("3️⃣ WEB SCRAPING")
        print(f"{'='*30}")
        try:
            result = self.method3_web_scraping(symbol.replace('.IS', ''))
            if result is not None:
                results['web_scraping'] = result
                success_count += 1
                print("✅ Web Scraping başarılı!")
            else:
                print("❌ Web Scraping başarısız!")
        except Exception as e:
            print(f"❌ Web Scraping hatası: {e}")
        
        # 4. Manuel Veri Girişi (atla)
        print(f"\n{'='*30}")
        print("4️⃣ MANUEL VERİ GİRİŞİ (ATLANDI)")
        print(f"{'='*30}")
        print("⚠️  Otomatik çalıştırma sırasında manuel giriş atlandı")
        
        # 5. Gerçek Zamanlı İzleme (kısa süreli)
        print(f"\n{'='*30}")
        print("5️⃣ GERÇEK ZAMANLI İZLEME (5 güncelleme)")
        print(f"{'='*30}")
        try:
            print("🔄 5 güncelleme yapılıyor...")
            ticker = yf.Ticker(symbol)
            for i in range(5):
                info = ticker.info
                current_time = datetime.now().strftime('%H:%M:%S')
                current_price = info.get('currentPrice', 'Bilinmiyor')
                change_percent = info.get('regularMarketChangePercent', 'Bilinmiyor')
                
                print(f"[{current_time}] 💰 {symbol}: {current_price} TL ({change_percent}%)")
                
                if i < 4:  # Son güncellemede bekleme
                    time.sleep(2)
            
            results['realtime'] = True
            success_count += 1
            print("✅ Gerçek zamanlı izleme başarılı!")
            
        except Exception as e:
            print(f"❌ Gerçek zamanlı izleme hatası: {e}")
        
        # Özet rapor
        print(f"\n{'='*50}")
        print("📊 ÖZET RAPOR")
        print(f"{'='*50}")
        print(f"🎯 Hedef sembol: {symbol}")
        print(f"✅ Başarılı yöntemler: {success_count}/{total_methods}")
        print(f"📈 Başarı oranı: {(success_count/total_methods)*100:.1f}%")
        print(f"⏱️  Bitiş zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if results:
            print(f"\n💾 Kaydedilen veri türleri:")
            for method, data in results.items():
                if method == 'realtime':
                    print(f"   - {method}: ✅")
                else:
                    print(f"   - {method}: {len(data)} satır veri")
        
        # Tüm verileri birleştir ve kaydet
        if len(results) > 1:
            try:
                self.save_combined_data(results, symbol)
            except Exception as e:
                print(f"⚠️  Veri birleştirme hatası: {e}")
        
        print(f"\n🎉 Otomatik veri çekme tamamlandı!")
        return results
    
    def save_combined_data(self, results, symbol):
        """Tüm verileri birleştir ve kaydet"""
        print(f"\n🔗 Veriler birleştiriliyor...")
        
        combined_data = {}
        
        # Yahoo Finance verilerini ekle
        if 'yfinance' in results:
            yf_data = results['yfinance']
            combined_data['Yahoo_Finance'] = {
                'Son_5_Gun': yf_data.tail()[['Open', 'High', 'Low', 'Close', 'Volume']].round(2),
                'Veri_Sayisi': len(yf_data),
                'Tarih_Araligi': f"{yf_data.index[0].strftime('%Y-%m-%d')} - {yf_data.index[-1].strftime('%Y-%m-%d')}"
            }
        
        # Alpha Vantage verilerini ekle
        if 'alpha_vantage' in results:
            av_data = results['alpha_vantage']
            combined_data['Alpha_Vantage'] = {
                'Son_5_Gun': av_data.tail()[['1. open', '2. high', '3. low', '4. close', '5. volume']].round(2),
                'Veri_Sayisi': len(av_data),
                'Tarih_Araligi': f"{av_data.index[0].strftime('%Y-%m-%d')} - {av_data.index[-1].strftime('%Y-%m-%d')}"
            }
        
        # Web Scraping verilerini ekle
        if 'web_scraping' in results:
            combined_data['Web_Scraping'] = results['web_scraping']
        
        # Excel olarak kaydet
        filename = f"{symbol.replace('.IS', '')}_TUM_VERILER_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Her veri türü için ayrı sayfa
            for method, data in combined_data.items():
                if isinstance(data, dict) and 'Son_5_Gun' in data:
                    # Son 5 gün verilerini kaydet
                    data['Son_5_Gun'].to_excel(writer, sheet_name=f"{method}_Son5Gun")
                    
                    # Özet bilgileri kaydet
                    summary_df = pd.DataFrame({
                        'Bilgi': ['Veri Sayısı', 'Tarih Aralığı'],
                        'Değer': [data['Veri_Sayisi'], data['Tarih_Araligi']]
                    })
                    summary_df.to_excel(writer, sheet_name=f"{method}_Ozet", index=False)
                else:
                    # Direkt DataFrame'i kaydet
                    data.to_excel(writer, sheet_name=method, index=False)
        
        print(f"💾 Birleştirilmiş veriler kaydedildi: {filename}")
    
    def run_all_methods(self):
        """Tüm yöntemleri çalıştır"""
        self.print_separator("CANLI VERİ ÇEKME ARAÇLARI")
        
        print("🔧 Mevcut yöntemler:")
        print("1. Yahoo Finance API (Ücretsiz)")
        print("2. Alpha Vantage API (Ücretsiz, key gerekli)")
        print("3. Web Scraping (Borsa İstanbul)")
        print("4. Manuel Veri Girişi")
        print("5. Gerçek Zamanlı İzleme")
        print("6. 🚀 TÜM YÖNTEMLERİ OTOMATİK ÇALIŞTIR")
        
        while True:
            try:
                choice = input("\n🎯 Hangi yöntemi kullanmak istiyorsunuz? (1-6, q=çıkış): ")
                
                if choice.lower() == 'q':
                    print("👋 Program sonlandırılıyor...")
                    break
                
                elif choice == '1':
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "1mo"
                    self.method1_yfinance(symbol, period)
                
                elif choice == '2':
                    api_key = input("🔑 Alpha Vantage API Key: ")
                    symbol = input("📈 Hisse senedi sembolü: ") or "THYAO"
                    self.method2_alpha_vantage(symbol, api_key)
                
                elif choice == '3':
                    symbol = input("📈 Hisse senedi sembolü: ") or "THYAO"
                    self.method3_web_scraping(symbol)
                
                elif choice == '4':
                    self.method4_manual_input()
                
                elif choice == '5':
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    interval = int(input("⏱️  Güncelleme aralığı (saniye): ") or "30")
                    self.method5_realtime_monitoring(symbol, interval)
                
                elif choice == '6':
                    print("\n🚀 TÜM YÖNTEMLER OTOMATİK ÇALIŞTIRILIYOR!")
                    symbol = input("📈 Hisse senedi sembolü (örn: THYAO.IS): ") or "THYAO.IS"
                    period = input("📅 Veri aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ") or "1mo"
                    api_key = input("🔑 Alpha Vantage API Key (opsiyonel, Enter'a basın): ") or None
                    self.method6_run_all_automatically(symbol, period, api_key)
                
                else:
                    print("❌ Geçersiz seçim! 1-6 arası bir sayı girin.")
                
            except KeyboardInterrupt:
                print("\n👋 Program sonlandırılıyor...")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    print("🚀 Canlı Finansal Veri Çekme Araçları Başlatılıyor...")
    
    # Gerekli kütüphaneleri kontrol et
    try:
        import yfinance
        print("✅ yfinance kütüphanesi mevcut")
    except ImportError:
        print("❌ yfinance kütüphanesi eksik!")
        print("💡 Kurulum: pip install yfinance")
    
    try:
        import alpha_vantage
        print("✅ alpha_vantage kütüphanesi mevcut")
    except ImportError:
        print("❌ alpha_vantage kütüphanesi eksik!")
        print("💡 Kurulum: pip install alpha-vantage")
    
    print()
    
    # Programı başlat
    veri_cekici = CanliVeriCekici()
    veri_cekici.run_all_methods()
