#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finansal Veri Analiz Web Uygulaması
Geliştiren: Çağatay Elaman
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import json
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

class FinansalAnalizWeb:
    def __init__(self):
        # Türk hisse senetleri
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
    
    def get_stock_data(self, symbol, period="1mo"):
        """Hisse senedi verilerini al"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if len(hist) > 0:
                # Veriyi JSON formatına çevir
                data = {
                    'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                    'open': hist['Open'].round(2).tolist(),
                    'high': hist['High'].round(2).tolist(),
                    'low': hist['Low'].round(2).tolist(),
                    'close': hist['Close'].round(2).tolist(),
                    'volume': hist['Volume'].tolist(),
                    'success': True
                }
                return data
            else:
                return {'success': False, 'error': 'Veri bulunamadı'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_stock_info(self, symbol):
        """Hisse senedi bilgilerini al"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            data = {
                'symbol': symbol,
                'company': info.get('longName', 'Bilinmiyor'),
                'current_price': info.get('currentPrice', 'Bilinmiyor'),
                'change_percent': info.get('regularMarketChangePercent', 'Bilinmiyor'),
                'market_cap': info.get('marketCap', 'Bilinmiyor'),
                'high_52w': info.get('fiftyTwoWeekHigh', 'Bilinmiyor'),
                'low_52w': info.get('fiftyTwoWeekLow', 'Bilinmiyor'),
                'success': True
            }
            return data
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def technical_analysis(self, symbol, period="3mo"):
        """Teknik analiz yap"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if len(hist) > 0:
                close_prices = hist['Close']
                
                # Teknik göstergeler
                ma20 = close_prices.rolling(window=20).mean()
                ma50 = close_prices.rolling(window=50).mean()
                
                # RSI
                delta = close_prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                # Bollinger Bands
                ma20_std = close_prices.rolling(window=20).std()
                upper_band = ma20 + (ma20_std * 2)
                lower_band = ma20 - (ma20_std * 2)
                
                # NaN değerleri None'a çevir (JSON için gerekli)
                def clean_nan_values(series):
                    return [None if pd.isna(x) else x for x in series]
                
                data = {
                    'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                    'close': close_prices.round(2).tolist(),
                    'ma20': clean_nan_values(ma20.round(2)),
                    'ma50': clean_nan_values(ma50.round(2)),
                    'rsi': clean_nan_values(rsi.round(2)),
                    'upper_band': clean_nan_values(upper_band.round(2)),
                    'lower_band': clean_nan_values(lower_band.round(2)),
                    'current_price': float(close_prices.iloc[-1]),
                    'current_rsi': float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                    'current_ma20': float(ma20.iloc[-1]) if not pd.isna(ma20.iloc[-1]) else None,
                    'current_ma50': float(ma50.iloc[-1]) if not pd.isna(ma50.iloc[-1]) else None,
                    'success': True
                }
                return data
            else:
                return {'success': False, 'error': 'Veri bulunamadı'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Web uygulaması instance'ı
analiz = FinansalAnalizWeb()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html', hisseler=analiz.turk_hisseleri)

@app.route('/api/stock_data')
def api_stock_data():
    """Hisse senedi verisi API"""
    symbol = request.args.get('symbol', 'THYAO.IS')
    period = request.args.get('period', '1mo')
    
    data = analiz.get_stock_data(symbol, period)
    return jsonify(data)

@app.route('/api/stock_info')
def api_stock_info():
    """Hisse senedi bilgisi API"""
    symbol = request.args.get('symbol', 'THYAO.IS')
    
    data = analiz.get_stock_info(symbol)
    return jsonify(data)

@app.route('/api/technical_analysis')
def api_technical_analysis():
    """Teknik analiz API"""
    symbol = request.args.get('symbol', 'THYAO.IS')
    period = request.args.get('period', '3mo')
    
    data = analiz.technical_analysis(symbol, period)
    return jsonify(data)

@app.route('/dashboard')
def dashboard():
    """Dashboard sayfası"""
    return render_template('dashboard.html', hisseler=analiz.turk_hisseleri)

@app.route('/analysis')
def analysis():
    """Analiz sayfası"""
    return render_template('analysis.html', hisseler=analiz.turk_hisseleri)

@app.route('/about')
def about():
    """Hakkında sayfası"""
    return render_template('about.html')

if __name__ == '__main__':
    # Templates klasörünü oluştur
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🚀 Finansal Veri Analiz Web Uygulaması Başlatılıyor...")
    print("🌐 Web sitesi: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
