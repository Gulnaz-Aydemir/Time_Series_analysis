# --- FAZ 3: LSTM MODELLEMESİ ---

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# 1. Veriyi Yükle ve Hazırla
try:
    df = pd.read_excel('MRC_Veri_Temiz.xlsx', 
                       sheet_name='Temiz_Veri', 
                       index_col='Tarih', 
                       parse_dates=True)
except FileNotFoundError:
    print("\nHATA: Veri dosyası bulunamadı!")
    exit()

df_7kw = df[df['Urun_Kodu'] == '7.5KW']['Satis_Adedi'].values.reshape(-1, 1)

# 2. Veriyi Ölçekle (Scaling)
# LSTM modelleri 0 ile 1 arasındaki değerlerle çalışır.
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df_7kw)

# 3. Veriyi Eğitme ve Test Etme Setlerine Ayırma
TEST_SIZE = 2 
train_data_len = len(scaled_data) - TEST_SIZE

train_data = scaled_data[0:train_data_len, :]
test_data = scaled_data[train_data_len:len(scaled_data), :]

# 4. LSTM için Veriyi Pencereleme (Windowing)
# LSTM'in anlayacağı 'x' (giriş) ve 'y' (çıkış) formatına çeviriyoruz.
# 4 dönem (hafta) verisi ile sonraki 1 dönemi tahmin etmeyi deneyeceğiz.
LOOK_BACK = 4 

def create_lstm_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

X_train, y_train = create_lstm_dataset(train_data, LOOK_BACK)
X_test, y_test = create_lstm_dataset(test_data, LOOK_BACK)

# LSTM modeline uygun 3D formatına çevirme: [örnekler, zaman adımları, özellikler]
# NOTE: Burada test verisi çok az olduğu için hata alabiliriz.
try:
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
except ValueError:
    print("\n--- UYARI: LSTM eğitimi için çok az veri var! ---")
    print("LSTM modeli veri azlığından dolayı düzgün çalışmayabilir, ancak deneyeceğiz.")


# 5. LSTM Modelini Kur ve Eğit
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(50, return_sequences=False, input_shape=(LOOK_BACK, 1)),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

print("\n--- LSTM Modeli Eğitiliyor (Kısa sürecek, veri az)... ---")
model.fit(X_train, y_train, epochs=20, batch_size=1, verbose=0) # Epoch sayısını az tuttuk

# 6. Tahmin Yap
predictions = model.predict(X_test)

# 7. Ölçeklemeyi Geri Al ve Hata Hesapla
predictions = scaler.inverse_transform(predictions)
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# 8. Hata Metriklerini Hesapla
rmse = np.sqrt(mean_squared_error(y_test, predictions))
mape = mean_absolute_percentage_error(y_test, predictions) * 100

print("\n=======================================================")
print("             LSTM MODEL SONUÇLARI (7.5KW)             ")
print("=======================================================")
print(f"1. RMSE (Hata Karekökü): {rmse:.2f}")
print(f"2. MAPE (OMYH): %{mape:.2f}")
print("-------------------------------------------------------")
print(f"Gerçek Satış (Son Tahmin): {y_test[-1][0]:.2f}")
print(f"LSTM Tahmini (Son Tahmin): {predictions[-1][0]:.2f}")