#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kaydedilen Keras Modelini Kullanma
"""

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

print("=== Kaydedilen Model Kullanımı ===")

# 1. Modeli yükle
print("1. Model yükleniyor...")
try:
    model = load_model("Hisse_regresyon_analizi.keras")
    print("✅ Model başarıyla yüklendi!")
    print(f"Model özeti:")
    model.summary()
except Exception as e:
    print(f"❌ Model yüklenirken hata: {e}")
    exit()

# 2. Örnek veri ile tahmin yap
print("\n2. Örnek tahminler yapılıyor...")

# Örnek veri (Min, Max, aof, Hacim, Sermaye, usd_try, bist_100, piyasa_degeri_tl, halka_acık_pd_tl)
ornek_veriler = [
    [3.70, 4.06, 3.86, 83486328, 26, 7.0531, 1.546, 480, 194],
    [2.81, 3.23, 3.05, 17666101, 27, 7.8222, 1.377, 379, 153],
    [11.75, 12.30, 12.00, 16255501, 120, 18.5272, 7.841, 1.416, 615]
]

# Veri normalizasyonu için scaler (gerçek verilerden)
# Not: Gerçek uygulamada eğitim verilerinden scaler'ı da kaydetmeniz gerekir
print("⚠️  Not: Gerçek uygulamada scaler'ı da kaydetmeniz gerekir")
print("Şimdilik manuel normalizasyon yapılıyor...")

# Basit normalizasyon (0-1 arasına)
ornek_veriler_norm = []
for veri in ornek_veriler:
    # Her sütun için basit normalizasyon
    norm_veri = []
    for i, deger in enumerate(veri):
        if i < 5:  # İlk 5 sütun (Min, Max, aof, Hacim, Sermaye)
            norm_veri.append(deger / 100)  # Basit normalizasyon
        else:  # Diğer sütunlar
            norm_veri.append(deger / 20)   # Basit normalizasyon
    ornek_veriler_norm.append(norm_veri)

# Tahminleri yap
print("\n3. Tahmin sonuçları:")
for i, (veri, norm_veri) in enumerate(zip(ornek_veriler, ornek_veriler_norm)):
    tahmin = model.predict(np.array([norm_veri]), verbose=0)[0][0]
    print(f"Örnek {i+1}:")
    print(f"  Giriş verileri: {veri}")
    print(f"  Tahmin edilen kapanış: {tahmin:.2f}")
    print()

# 4. Model hakkında bilgi
print("4. Model bilgileri:")
print(f"- Model katman sayısı: {len(model.layers)}")
print(f"- Giriş şekli: {model.input_shape}")
print(f"- Çıkış şekli: {model.output_shape}")
print(f"- Toplam parametre sayısı: {model.count_params():,}")

print("\n=== Model kullanımı tamamlandı! ===")
print("💡 İpucu: Gerçek uygulamada scaler'ı da kaydetmeyi unutmayın!")
