# 🌐 Finansal Veri Analiz Web Uygulaması

Modern web teknolojileri ile geliştirilmiş, Borsa İstanbul hisse senetlerini analiz eden profesyonel web platformu.

## 🚀 Özellikler

### 📊 Ana Sayfa
- **Canlı Veri Görüntüleme**: Yahoo Finance API ile gerçek zamanlı hisse senedi verileri
- **İnteraktif Grafikler**: Chart.js ile modern ve responsive grafikler
- **Hisse Senedi Seçimi**: 15+ popüler Türk hisse senedi
- **Veri Aralığı Seçimi**: 1 gün ile 1 yıl arası analiz

### 📈 Dashboard
- **İstatistik Kartları**: Mevcut fiyat, RSI, trend sinyali
- **Çoklu Grafikler**: Fiyat, RSI, hacim, Bollinger Bands
- **Teknik Analiz Özeti**: Detaylı teknik göstergeler ve sinyaller
- **Gerçek Zamanlı Güncelleme**: Tek tıkla dashboard yenileme

### 🔧 Teknik Özellikler
- **Flask Backend**: Python tabanlı güçlü web framework
- **Responsive Tasarım**: Bootstrap 5 ile mobil uyumlu
- **Modern UI/UX**: Glassmorphism tasarım trendi
- **Chart.js Entegrasyonu**: Profesyonel grafik kütüphanesi

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)

### Adım 1: Projeyi İndirin
```bash
git clone <repository-url>
cd finansal-analiz-hisse-tahmini-main
```

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv .venv
```

### Adım 3: Sanal Ortamı Aktifleştirin
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Adım 4: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 5: Uygulamayı Çalıştırın
```bash
python web_app.py
```

### Adım 6: Tarayıcıda Açın
```
http://localhost:5000
```

## 📱 Kullanım

### Ana Sayfa
1. **Hisse Senedi Seçin**: Dropdown menüden istediğiniz hisseyi seçin
2. **Veri Aralığı Belirleyin**: 1 gün ile 1 yıl arası seçim yapın
3. **Veri Yükleyin**: "Veri Yükle" butonuna tıklayın
4. **Grafikleri İnceleyin**: Fiyat grafiği ve hisse bilgileri görüntülenir

### Dashboard
1. **Dashboard'a Gidin**: Ana sayfadan "Dashboard'a Git" butonuna tıklayın
2. **Ayarları Yapın**: Hisse senedi ve veri aralığı seçin
3. **Dashboard'ı Güncelleyin**: "Dashboard'ı Güncelle" butonuna tıklayın
4. **Analizleri İnceleyin**: Çoklu grafikler ve teknik analiz özeti

## 🏗️ Proje Yapısı

```
finansal-analiz-hisse-tahmini-main/
├── web_app.py                 # Ana Flask uygulaması
├── requirements.txt           # Python bağımlılıkları
├── templates/                 # HTML template'leri
│   ├── index.html            # Ana sayfa
│   ├── dashboard.html        # Dashboard sayfası
│   ├── analysis.html         # Analiz sayfası
│   └── about.html            # Hakkında sayfası
├── Finansal_Veriler/         # Organize edilmiş Excel dosyaları
│   ├── Detayli_Veriler/
│   ├── Teknik_Analiz/
│   ├── Tum_Veriler/
│   └── ...
├── gelismis_veri_cekme.py    # Gelişmiş veri çekme araçları
├── dosya_duzenleme.py        # Dosya organizasyon araçları
└── README_WEB.md             # Bu dosya
```

## 🔌 API Endpoints

### Hisse Senedi Verisi
```
GET /api/stock_data?symbol=THYAO.IS&period=1mo
```

### Hisse Senedi Bilgisi
```
GET /api/stock_info?symbol=THYAO.IS
```

### Teknik Analiz
```
GET /api/technical_analysis?symbol=THYAO.IS&period=3mo
```

## 📊 Desteklenen Hisse Senetleri

| Kod | Sembol | Şirket |
|-----|--------|---------|
| THYAO | THYAO.IS | Türk Hava Yolları |
| GARAN | GARAN.IS | Garanti Bankası |
| AKBNK | AKBNK.IS | Akbank |
| ISCTR | ISCTR.IS | İş Bankası |
| ASELSAN | ASELSAN.IS | Aselsan |
| KRDMD | KRDMD.IS | Kardemir |
| SASA | SASA.IS | Sasa |
| BIMAS | BIMAS.IS | BİM |
| MGROS | MGROS.IS | Migros |
| AEFES | AEFES.IS | Anadolu Efes |
| KCHOL | KCHOL.IS | Koç Holding |
| SAHOL | SAHOL.IS | Sabancı Holding |
| TUPRS | TUPRS.IS | Tüpraş |
| EREGL | EREGL.IS | Ereğli Demir Çelik |

## 🎨 Tasarım Özellikleri

### Renk Paleti
- **Ana Renk**: #667eea (Mavi)
- **İkincil Renk**: #764ba2 (Mor)
- **Arka Plan**: Gradient (Mavi → Mor)
- **Kartlar**: Glassmorphism efekti

### Responsive Tasarım
- **Mobil**: 100% uyumlu
- **Tablet**: Optimize edilmiş
- **Desktop**: Tam özellikli

### Modern UI Elementleri
- **Glassmorphism**: Şeffaf, bulanık kartlar
- **Gradient Buttons**: Modern buton tasarımı
- **Icon Integration**: Font Awesome ikonları
- **Smooth Animations**: Hover efektleri

## 🔒 Güvenlik

- **Input Validation**: Tüm kullanıcı girdileri doğrulanır
- **Error Handling**: Kapsamlı hata yönetimi
- **Safe API Calls**: Güvenli API istekleri
- **XSS Protection**: Cross-site scripting koruması

## 🚀 Gelecek Özellikler

- [ ] **Kullanıcı Hesapları**: Kayıt ve giriş sistemi
- [ ] **Portföy Takibi**: Kişisel hisse portföyü
- [ ] **Alarm Sistemi**: Fiyat alarmları
- [ ] **Sosyal Özellikler**: Yorum ve paylaşım
- [ ] **Mobil Uygulama**: iOS ve Android uygulamaları
- [ ] **Gelişmiş Analiz**: Daha fazla teknik gösterge
- [ ] **Backtesting**: Strateji test sistemi

## 🐛 Sorun Giderme

### Uygulama Başlamıyor
```bash
# Sanal ortamın aktif olduğundan emin olun
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```