#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finansal Veri Analizi ve Tahmin Projesi
Geliştiren: Çağatay Elaman
"""

import pandas as pd
import numpy as np
import seaborn as sbn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler 
from keras.optimizers import Adam

print("=== Finansal Veri Analizi ve Tahmin Projesi ===")
    print("Geliştiren: Çağatay Elaman")
    print()

# 1. Veri Yükleme
print("1. Veri yükleniyor...")
exel_verisi = pd.read_excel("dnıs.xlsx")
print(f"Veri seti yüklendi. Boyut: {exel_verisi.shape}")
print()

# 2. Veri Temizleme
print("2. Veri temizleniyor...")
exel_verisi["usd_try"] = exel_verisi["usd_try"].str.replace(",",".").astype(float)
exel_verisi["Kapanış"] = exel_verisi["Kapanış"].str.replace(",",".").astype(float)
exel_verisi["Min"] = exel_verisi["Min"].str.replace(",",".").astype(float)
exel_verisi["Max"] = exel_verisi["Max"].str.replace(",",".").astype(float)
exel_verisi["aof"] = exel_verisi["aof"].str.replace(",",".").astype(float)
exel_verisi["Hacim"] = exel_verisi["Hacim"].str.replace(".","").astype(float)

# Null değer kontrolü
print("Null değer kontrolü yapılıyor...")
null_kontrol = exel_verisi.isnull().any()
null_sutunlar = null_kontrol[null_kontrol].index
print(f"Null değer olan sütunlar: {list(null_sutunlar)}")

toplam_null_deger_sayisi = exel_verisi.isnull().sum().sum()
print(f"Toplam null değer sayısı: {toplam_null_deger_sayisi}")

# Null değerli satırları sil
if toplam_null_deger_sayisi > 0:
    exel_verisi = exel_verisi.dropna()
    print("Null değerli satırlar silindi.")

print(f"Temizlenmiş veri seti boyutu: {exel_verisi.shape}")
print()

# 3. Veri Görselleştirme
print("3. Veri görselleştirme yapılıyor...")
plt.figure(figsize=(12, 8))

# Korelasyon matrisi
plt.subplot(2, 2, 1)
cor = exel_verisi.corr()
sbn.heatmap(cor, annot=True, cmap="coolwarm", linewidths=.5)
plt.title("Korelasyon Matrisi")

# Kapanış vs Hacim
plt.subplot(2, 2, 2)
plt.scatter(exel_verisi["Kapanış"], exel_verisi["Hacim"])
plt.xlabel("Kapanış")
plt.ylabel("Hacim")
plt.title("Kapanış vs Hacim")

# Kapanış vs USD/TRY
plt.subplot(2, 2, 3)
plt.scatter(exel_verisi["Kapanış"], exel_verisi["usd_try"])
plt.xlabel("Kapanış")
plt.ylabel("USD/TRY")
plt.title("Kapanış vs USD/TRY")

# Kapanış vs BIST100
plt.subplot(2, 2, 4)
plt.scatter(exel_verisi["Kapanış"], exel_verisi["bist_100"])
plt.xlabel("Kapanış")
plt.ylabel("BIST100")
plt.title("Kapanış vs BIST100")

plt.tight_layout()
plt.savefig("veri_analizi.png", dpi=300, bbox_inches='tight')
print("Görselleştirme kaydedildi: veri_analizi.png")
print()

# 4. Model Eğitimi
print("4. Model eğitimi başlıyor...")

# Veri setini hazırla
y_degeri = exel_verisi["Kapanış"].values
x_degerleri = exel_verisi[[ "Min", "Max", "aof", "Hacim", "Sermaye",
    "usd_try", "bist_100", "piyasa_degeri_tl", "halka_acık_pd_tl"]].values

print(f"X değişkenleri boyutu: {x_degerleri.shape}")
print(f"Y değişkeni boyutu: {y_degeri.shape}")

# Veri setini böl
x_train, x_test, y_train, y_test = train_test_split(x_degerleri, y_degeri, test_size=0.60, random_state=42)
print(f"Eğitim seti boyutu: {x_train.shape}")
print(f"Test seti boyutu: {x_test.shape}")

# Veri normalizasyonu
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Model oluştur
print("Model oluşturuluyor...")
model = Sequential()
model.add(Dense(5, activation="relu"))
model.add(Dense(5, activation="relu"))
model.add(Dense(5, activation="relu"))
model.add(Dense(5, activation="relu"))
model.add(Dense(5, activation="relu"))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mse")
print("Model eğitiliyor (95 epoch)...")
model.fit(x_train, y_train, epochs=95, verbose=0)

print("Model eğitimi tamamlandı!")
print()

# 5. Model Değerlendirme
print("5. Model değerlendiriliyor...")

# Eğitim hatası
train_loss = model.evaluate(x_train, y_train, verbose=0)
print(f"Eğitim hatası (MSE): {train_loss:.6f}")

# Test tahminleri
test_tahminleri = model.predict(x_test, verbose=0)
tahmin_degerleri = pd.DataFrame({
    "Gerçek değerler": y_test.flatten(),
    "Model Tahmini": test_tahminleri.flatten()
})

# MAE hesapla
mae = mean_absolute_error(tahmin_degerleri["Gerçek değerler"], tahmin_degerleri["Model Tahmini"])
print(f"Ortalama Mutlak Hata (MAE): {mae:.6f}")

# Tahmin grafiği
plt.figure(figsize=(10, 6))
plt.scatter(tahmin_degerleri["Gerçek değerler"], tahmin_degerleri["Model Tahmini"], alpha=0.6)
plt.plot([tahmin_degerleri["Gerçek değerler"].min(), tahmin_degerleri["Gerçek değerler"].max()], 
         [tahmin_degerleri["Gerçek değerler"].min(), tahmin_degerleri["Gerçek değerler"].max()], 
         'r--', lw=2)
plt.xlabel("Gerçek Değerler")
plt.ylabel("Model Tahmini")
plt.title("Gerçek vs Tahmin Değerleri")
plt.grid(True, alpha=0.3)
plt.savefig("tahmin_grafigi.png", dpi=300, bbox_inches='tight')
print("Tahmin grafiği kaydedildi: tahmin_grafigi.png")
print()

# 6. Yeni Tahminler
print("6. Yeni tahminler yapılıyor...")

# Test verileri
yeni_tahmin1 = [[3.70, 4.06, 3.86, 83486328, 26, 7.0531, 1.546, 480, 194]]
yeni_tahmin2 = [[2.81, 3.23, 3.05, 17666101, 27, 7.8222, 1.377, 379, 153]]
yeni_tahmin3 = [[11.75, 12.30, 12, 16255501, 120, 18.5272, 7.841, 1.416, 615]]

# Tahminleri yap
tahmin1 = model.predict(scaler.transform(yeni_tahmin1), verbose=0)[0][0]
tahmin2 = model.predict(scaler.transform(yeni_tahmin2), verbose=0)[0][0]
tahmin3 = model.predict(scaler.transform(yeni_tahmin3), verbose=0)[0][0]

print(f"Test 1 - Gerçek: 4.06, Tahmin: {tahmin1:.2f}")
print(f"Test 2 - Gerçek: 3.20, Tahmin: {tahmin2:.2f}")
print(f"Test 3 - Gerçek: 11.83, Tahmin: {tahmin3:.2f}")
print()

# 7. Model Kaydetme
print("7. Model kaydediliyor...")
model.save("Hisse_regresyon_analizi.keras")
print("Model kaydedildi: Hisse_regresyon_analizi.keras")

print()
print("=== Analiz tamamlandı! ===")
print("Sonuçlar:")
print(f"- Veri seti boyutu: {exel_verisi.shape}")
print(f"- Model eğitim hatası: {train_loss:.6f}")
print(f"- Test MAE: {mae:.6f}")
print(f"- Model başarıyla kaydedildi")
