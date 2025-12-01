# --- FAZ 3: PROPHET MODELLEMESİ ---

import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import numpy as np

print("--- PROPHET MODELLEME BAŞLADI (7.5KW Ürünü İçin) ---")

# 1. Veriyi Yükle ve Hazırla (XLSX Okuma Düzeltmesi)
try:
    df = pd.read_excel('MRC_Veri_Temiz.xlsx', 
                       sheet_name='Temiz_Veri', 
                       index_col='Tarih', 
                       parse_dates=True)
except FileNotFoundError:
    print("\nHATA: 'MRC_Veri_Temiz.xlsx' dosyası bulunamadı!")
    exit()

# 2. Analiz için Sadece 7.5KW Ürününü Ayır ve Prophet Formatına Çevir
df_7kw = df[df['Urun_Kodu'] == '7.5KW']

# Prophet için sütun adlarını 'ds' (datestamp) ve 'y' (target) olarak değiştirmeliyiz
df_prophet = df_7kw.reset_index().rename(columns={'Tarih': 'ds', 'Satis_Adedi': 'y'})

# 3. Veriyi Eğitme ve Test Etme Setlerine Ayırma
TEST_SIZE = 2 
train_data_p = df_prophet.iloc[:-TEST_SIZE] # İlk 22 dönemi al (Eğitim)
test_data_p = df_prophet.iloc[-TEST_SIZE:]  # Son 2 dönemi (Aralık) al (Test)

print(f"Prophet Eğitim Seti: {len(train_data_p)} | Test Seti: {len(test_data_p)}")

# 4. Prophet Modelini Kur ve Eğit
# Model kuruluyor: Yıllık mevsimsellik aramasını istiyoruz (weekly_seasonality=False çünkü veri bi-weekly)
model_p = Prophet(
    yearly_seasonality=True, 
    weekly_seasonality=False, 
    daily_seasonality=False
)

print("\n--- Prophet Modeli Eğitiliyor (Bu kısım hızlıdır)... ---")
model_p.fit(train_data_p)

# 5. Gelecekteki Tahmin Çerçevesini Oluştur
# Tahmin yapacağımız 2 dönemi (geleceği) tanımlıyoruz
future = model_p.make_future_dataframe(periods=TEST_SIZE, freq='D') # Günlük frekans verelim ki, sonra filtreleyebilelim

# 6. Tahmin Yap
forecast = model_p.predict(future)

# 7. Sadece Test Dönemine Ait Tahminleri Ayır
# Tahmin tablosundan sadece test ettiğimiz son 2 döneme ait satırları alalım
forecast_test = forecast.tail(TEST_SIZE)
forecast_test_values = forecast_test['yhat'].values

# 8. Hata Metriklerini Hesapla
rmse = np.sqrt(mean_squared_error(test_data_p['y'], forecast_test_values))
mape = mean_absolute_percentage_error(test_data_p['y'], forecast_test_values) * 100

print("\n=======================================================")
print("             PROPHET MODEL SONUÇLARI (7.5KW)           ")
print("=======================================================")
print(f"1. RMSE (Hata Karekökü): {rmse:.2f}")
print(f"2. MAPE (OMYH): %{mape:.2f}")
print("-------------------------------------------------------")

# 9. Tahmin ve Gerçek Değerleri Göster
results_prophet = pd.DataFrame({
    'Gercek_Satis': test_data_p['y'].values, 
    'Prophet_Tahmini': forecast_test_values.round(2)
})
print(results_prophet)

# 10. Grafik Çıktısı (Prophet'in Bileşenler Grafiği çok değerlidir)
fig_components = model_p.plot_components(forecast)
fig_components.savefig('CIKTI_PROPHET_Bilesenler.png')
print("Prophet'in bileşenler grafiği 'CIKTI_PROPHET_Bilesenler.png' olarak kaydedildi.")