#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mevcut Excel Dosyalarını Düzenleme ve Klasörleme
Geliştiren: Çağatay Elaman
"""

import os
import shutil
from datetime import datetime
import glob

class DosyaDuzenleyici:
    def __init__(self):
        # Klasör yapısı
        self.folders = {
            'base': 'Finansal_Veriler',
            'detayli': 'Detayli_Veriler',
            'teknik': 'Teknik_Analiz',
            'karsilastirma': 'Karsilastirmalar',
            'tum_veriler': 'Tum_Veriler',
            'manuel': 'Manuel_Veriler',
            'canli': 'Canli_Veriler',
            'orijinal': 'Orijinal_Veriler'
        }
        
        # Dosya türlerini belirle
        self.file_types = {
            'detayli': ['_detayli_veri_'],
            'teknik': ['_teknik_analiz_'],
            'tum_veriler': ['_TUM_VERILER_'],
            'canli': ['_canli_veri_'],
            'karsilastirma': ['karsilastirma_'],
            'orijinal': ['dnıs.xlsx', 'veri.xlsx']
        }
    
    def print_separator(self, title):
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def setup_folders(self):
        """Klasör yapısını oluştur"""
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
    
    def find_excel_files(self):
        """Mevcut Excel dosyalarını bul"""
        excel_files = []
        
        # Tüm .xlsx dosyalarını bul
        for file in glob.glob("*.xlsx"):
            if os.path.isfile(file):
                excel_files.append(file)
        
        return excel_files
    
    def categorize_file(self, filename):
        """Dosyayı kategorize et"""
        filename_lower = filename.lower()
        
        for category, patterns in self.file_types.items():
            for pattern in patterns:
                if pattern.lower() in filename_lower:
                    return category
        
        # Eğer hiçbir kategoriye uymuyorsa, orijinal olarak sınıflandır
        return 'orijinal'
    
    def get_destination_folder(self, category, filename):
        """Hedef klasör yolunu belirle"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if category in self.folders:
            return os.path.join(self.folders['base'], self.folders[category], today)
        else:
            return os.path.join(self.folders['base'], today)
    
    def move_file(self, source_file, destination_folder):
        """Dosyayı taşı"""
        try:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            destination_path = os.path.join(destination_folder, os.path.basename(source_file))
            
            # Eğer hedef dosya zaten varsa, üzerine yazma
            if os.path.exists(destination_path):
                base_name = os.path.splitext(os.path.basename(source_file))[0]
                extension = os.path.splitext(source_file)[1]
                counter = 1
                while os.path.exists(destination_path):
                    new_name = f"{base_name}_v{counter}{extension}"
                    destination_path = os.path.join(destination_folder, new_name)
                    counter += 1
            
            shutil.move(source_file, destination_path)
            return destination_path
        except Exception as e:
            print(f"❌ {source_file} taşınırken hata: {e}")
            return None
    
    def organize_files(self):
        """Dosyaları organize et"""
        self.print_separator("DOSYA ORGANİZASYONU BAŞLATILIYOR")
        
        # Klasörleri oluştur
        self.setup_folders()
        
        # Excel dosyalarını bul
        excel_files = self.find_excel_files()
        
        if not excel_files:
            print("📭 Hiç Excel dosyası bulunamadı!")
            return
        
        print(f"📊 {len(excel_files)} Excel dosyası bulundu:")
        for file in excel_files:
            print(f"   📄 {file}")
        
        print(f"\n🔄 Dosyalar organize ediliyor...")
        
        # Dosyaları kategorize et ve taşı
        moved_files = {}
        for file in excel_files:
            category = self.categorize_file(file)
            destination_folder = self.get_destination_folder(category, file)
            
            print(f"\n📁 {file} → {category} kategorisi")
            print(f"   📂 Hedef: {destination_folder}")
            
            destination_path = self.move_file(file, destination_folder)
            
            if destination_path:
                if category not in moved_files:
                    moved_files[category] = []
                moved_files[category].append(destination_path)
                print(f"   ✅ Taşındı: {destination_path}")
            else:
                print(f"   ❌ Taşınamadı!")
        
        # Özet rapor
        self.print_summary(moved_files)
    
    def print_summary(self, moved_files):
        """Özet rapor göster"""
        self.print_separator("ORGANİZASYON TAMAMLANDI")
        
        total_moved = sum(len(files) for files in moved_files.values())
        print(f"🎉 Toplam {total_moved} dosya organize edildi!")
        
        print(f"\n📊 Kategori Bazında Dağılım:")
        for category, files in moved_files.items():
            print(f"   📁 {category.title()}: {len(files)} dosya")
            for file in files:
                print(f"      📄 {os.path.basename(file)}")
        
        print(f"\n📂 Ana Klasör: {self.folders['base']}")
        print(f"💡 Dosyalar tarih bazında organize edildi!")
    
    def show_current_structure(self):
        """Mevcut klasör yapısını göster"""
        self.print_separator("MEVCUT KLASÖR YAPISI")
        
        base_folder = self.folders['base']
        if not os.path.exists(base_folder):
            print("❌ Henüz klasör yapısı oluşturulmamış!")
            return
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        print(f"📂 Ana Klasör: {base_folder}")
        print(f"📅 Tarih: {today}")
        print()
        
        total_files = 0
        for folder_name, folder_path in self.folders.items():
            if folder_name != 'base':
                full_path = os.path.join(base_folder, folder_path, today)
                print(f"📁 {folder_name.title()}: {full_path}")
                
                if os.path.exists(full_path):
                    files = [f for f in os.listdir(full_path) if f.endswith('.xlsx')]
                    print(f"      📄 {len(files)} Excel dosyası")
                    total_files += len(files)
                    
                    # Dosya isimlerini göster
                    for file in files[:5]:  # İlk 5 dosyayı göster
                        print(f"         - {file}")
                    if len(files) > 5:
                        print(f"         ... ve {len(files) - 5} dosya daha")
                else:
                    print(f"      📭 Klasör boş")
        
        print(f"\n💡 Toplam Excel dosyası: {total_files}")
    
    def run_menu(self):
        """Ana menü"""
        self.print_separator("DOSYA ORGANİZASYON ARAÇLARI")
        
        print("🔧 Mevcut işlemler:")
        print("1. 📁 Dosyaları Organize Et")
        print("2. 📊 Mevcut Klasör Yapısını Göster")
        print("3. 🚀 Otomatik Organizasyon")
        
        while True:
            try:
                choice = input("\n🎯 Hangi işlemi yapmak istiyorsunuz? (1-3, q=çıkış): ")
                
                if choice.lower() == 'q':
                    print("👋 Program sonlandırılıyor...")
                    break
                
                elif choice == '1':
                    self.organize_files()
                
                elif choice == '2':
                    self.show_current_structure()
                
                elif choice == '3':
                    print("\n🚀 Otomatik organizasyon başlatılıyor...")
                    self.organize_files()
                    print("\n🎉 Otomatik organizasyon tamamlandı!")
                
                else:
                    print("❌ Geçersiz seçim! 1-3 arası bir sayı girin.")
                
            except KeyboardInterrupt:
                print("\n👋 Program sonlandırılıyor...")
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    print("🚀 Dosya Organizasyon Araçları Başlatılıyor...")
    
    # Programı başlat
    duzenleyici = DosyaDuzenleyici()
    duzenleyici.run_menu()
