# --- FAZ 2: SARIMA MODELLEMESİ ---

# 1. Gerekli Kütüphaneleri Çağır
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima 

print("--- SARIMA MODELLEME BAŞLADI (7.5KW Ürünü İçin) ---")

# 2. Veriyi Yükle ve Hata Düzeltmesi (XLSX Okuma)
# Not: CSV bulunamadığı için, elle düzenlediğimiz XLSX dosyasını okuyoruz.
try:
    df = pd.read_excel('MRC_Veri_Temiz.xlsx', 
                       sheet_name='Temiz_Veri', 
                       index_col='Tarih', 
                       parse_dates=True)
except FileNotFoundError:
    print("\nHATA: 'MRC_Veri_Temiz.xlsx' dosyası bulunamadı! Lütfen dosyanın klasörde olduğundan emin olun.")
    exit()

# 3. Analiz için Sadece 7.5KW Ürününü Ayır
# Sadece Satış Adedi sütununu alıyoruz ve '7.5KW'a ait olanları seçiyoruz.
df_7kw = df[df['Urun_Kodu'] == '7.5KW']['Satis_Adedi']

# 4. Veriyi Eğitme ve Test Etme Setlerine Ayırma (Train/Test Split)
# Son 2 dönemi (Aralık ayı) test için ayırıyoruz (Hocaya göstermek için).
TEST_SIZE = 2 
train_data = df_7kw.iloc[:-TEST_SIZE] # İlk 22 dönemi al (Eğitim)
test_data = df_7kw.iloc[-TEST_SIZE:]  # Son 2 dönemi (Aralık) al (Test)

print(f"Toplam Veri: {len(df_7kw)} | Eğitim Seti: {len(train_data)} | Test Seti: {len(test_data)}")
print("\n--- auto_arima İle En İyi SARIMA Modeli Aranıyor (Bu işlem biraz sürebilir)... ---")


# 5. auto_arima İle En İyi SARIMA Modelini Bul
# m=12: Mevsimsel periyodu 12 olarak varsayıyoruz (6 aylık/yarı-yıllık desen arıyoruz)
# stepwise=True: En iyi modeli hızlıca bulmak için akıllı arama yapar
best_model = auto_arima(train_data, 
                        seasonal=True, 
                        m=12,
                        suppress_warnings=True, 
                        stepwise=True, 
                        error_action='ignore')

# 6. Sonuçları Ekrana Yazdır
print("\n=======================================================")
print("             SARIMA MODEL SONUÇLARI (7.5KW)           ")
print("=======================================================")

# Modelin detaylı istatistiksel özetini yazdır (Bu çıktıyı bana göndereceksin)
print(best_model.summary()) 

# Modelin Hata Metriğini (AIC) yakala (Karşılaştırma tablomuzdaki metrik)
AIC_value = best_model.aic()
print(f"\n-> EN İYİ MODELİN AIC DEĞERİ: {AIC_value:.2f}")
print("=======================================================")

# 7. Tahmin Yap ve Karşılaştır (Görsel Çıktı)
forecast_periods = len(test_data)
forecast = best_model.predict(n_periods=forecast_periods)

forecast_series = pd.Series(forecast, index=test_data.index)

print("\n--- SARIMA Tahmini ve Gerçek Değerler (Son 2 Dönem) ---")
results_df = pd.DataFrame({'Gercek_Satis': test_data, 'SARIMA_Tahmini': forecast_series.round(2)})
print(results_df)

# Grafik Çıktısı (Rapor için gerekli)
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data, label='Eğitim Verisi (Train)')
plt.plot(test_data.index, test_data, label='Gerçek Test Verisi (Actual)', marker='o')
plt.plot(forecast_series.index, forecast_series, label='SARIMA Tahmini (Forecast)', marker='x')
plt.title(f'7.5KW Ürünü - SARIMA Tahmini (AIC: {AIC_value:.2f})')
plt.legend()
plt.savefig('CIKTI_SARIMA_Tahmin.png')

print("Grafik başarıyla 'CIKTI_SARIMA_Tahmin.png' olarak kaydedildi.")

# --- EKSİK METRİK HESAPLAMA VE NAN HATASI DÜZELTME ---

from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import numpy as np

# 1. SARIMA Tahmininin Doğru Metriklerini Hesapla
# Tahmin (forecast) bir numpy array olarak gelir, Test verisi (test_data) ise pandas Serisi.
# NaN hatasını gidermek için sadece sayısal değerleri alıp karşılaştırıyoruz.

# Hata Hesaplamaları
rmse = np.sqrt(mean_squared_error(test_data, forecast))
mape = mean_absolute_percentage_error(test_data, forecast) * 100 # Yüzde olarak göster
mae = np.mean(np.abs(test_data - forecast)) # MAE'yi manuel hesaplayalım

print("\n\n--- SARIMA PERFORMANS METRİKLERİ ---")
print(f"1. RMSE (Hata Karekökü): {rmse:.2f}")
print(f"2. MAE (Ortalama Mutlak Hata): {mae:.2f}")
print(f"3. MAPE (OMYH): %{mape:.2f}")
print("------------------------------------------")

# Karşılaştırma Tablosu Özetini hazırlıyoruz
# BHO(6) 7.5KW için OMYH: 14.76'ydı. Hedefimiz 14.76'nın altına inmek.