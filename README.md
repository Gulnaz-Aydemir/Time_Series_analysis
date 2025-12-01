# 🏆 Bir Türk KOBİ'sinde Endüstriyel Talep Tahmini: Klasik Zaman Serisi Analizinden Yapay Zeka Modellerine Bir Vaka Çalışması

## ⚠️ BAŞLAMADAN ÖNCE KRİTİK NOT:
Lütfen tüm PNG dosyalarınızı (`CIKTI_1...png`, `CIKTI_2...png`, vb.) projenizin ana klasöründe bulunan **Images** adlı bir alt klasöre taşıyın. Aksi takdirde görseller görünmeyecektir.

## 🌟 Proje Özeti

Bu çalışma, **MRC Asansör Mühendislik** firmasının kritik ürün talebini tahmin etmeyi amaçlamaktadır. Proje, kısıtlı veri koşullarında, Geleneksel yöntemlerin hata oranlarını, modern **Gelişmiş İstatistiksel** ve **Yapay Zeka** modellerinin performansını karşılaştırmıştır.

**Kilit Bulgu:** Proje, $n=24$ gibi kısıtlı veri setlerinde, büyük hesaplama gücü gerektiren Derin Öğrenme (LSTM) modelleri yerine, **SARIMA** gibi Gelişmiş İstatistiksel Modellerin en güvenilir çözümü sunduğunu kanıtlamıştır.

## Hazırlayan
* **Gülnaz AYDEMİR** (220204019)
* **Ostim Teknik Üniversitesi** (2025)

## 1. Veri, Kapsam ve Özgünlük

| Kategori | Detay | Özgünlük Vurgusu |
| :--- | :--- | :--- |
| **Firma** | MRC Asansör Mühendislik / Ostim | **Gerçek KOBİ Vaka Analizi:** Sahadan alınan veriye dayanmaktadır. |
| **Hedef Ürün** | 7.5 KW İnverterli Kumanda Sistemi | **B2B Endüstriyel Ürün:** Spesifik sanayi ürününe odaklanılmıştır. |
| **Veri Kısıtlılığı**| 24 Dönemlik (Çift Haftalık) Veri | **Kısıtlı ve Gürültülü Veri:** Modeller için teknik bir zorluk teşkil etmiştir. |
| **Baseline** | BHO/ES (Basit Hareketli Ortalama) | Mevcut en iyi performans **%14.76 MAPE**. |

***

## 2. Veri Analizi ve Problem İspatı (EDA)

### 2.1. Toplu Zaman Serisi ve Korelasyon
Verinin ne kadar oynak (volatile) olduğunu ve üç ürünün talep yapısındaki keskin iniş çıkışları gösteren genel görünüm.
![Tüm Ürünlerin Satış Serisi](Images/CIKTI_1_Tum_Urunler_Zaman_Serisi.png)

### 2.2. Bileşenlere Ayırma
Zaman serisi ayrıştırması, klasik analizlerin aksine, veride anlamlı **dalgalı Trend** ve **Mevsimsellik** sinyallerinin bulunduğunu kanıtlamıştır.
![Zaman Serisi Bileşenlerine Ayrıştırma (Trend ve Mevsimsellik)](Images/CIKTI_2_7.5KW_Bilesenler.png)

***

## 3. Modelleme ve Nihai Bulgular

### 3.1. Modeller Arası Performans Tablosu

| Model | Kategori | MAPE (OMYH) | RMSE | AIC / Bulgu |
| :--- | :--- | :--- | :--- | :--- |
| **BHO/ES (Baseline)** | Geleneksel | %14.76 | 3.20 | Başlangıç Referansı. |
| **SARIMA** | **KAZANAN** | **%12.38** | **2.10** | **EN DÜŞÜK HATA ve EN İYİ UYUM** |
| **Prophet** | Makine Öğrenmesi | %34.45 | 7.67 | Veri azlığı nedeniyle **aşırı düzleştirme** ile başarısız. |
| **LSTM** | Derin Öğrenme | Uygulanamadı | Uygulanamadı | **Veri Kısıtlılığı** ($n=24$) nedeniyle matematiksel hata. |

### 3.2. SARIMA Tahmin Başarısı ve Görsel Kanıt

En iyi performansı gösteren SARIMA'nın, Gerçek Değerler'e ne kadar yaklaştığını gösteren görsel kanıt.
![SARIMA Modelinin Gerçek Değerler ile Tahmin Karşılaştırması](Images/CIKTI_SARIMA_Tahmin.png)

### 3.3. Kilit Endüstriyel Çıkarım

**KOBİ Veri Kısıtlılığı Kuralı:** Kısıtlı veriye sahip KOBİ'ler için, yüksek hesaplama gücü isteyen Yapay Zeka (LSTM, Prophet) modelleri yerine, veri yapısına odaklanan **Gelişmiş İstatistiksel Modeller (SARIMA)** en güvenilir çözümü sunmuştur.

**Kazanım:** Tahmin hatası **%14.76'dan %12.38'e** düşürülerek firma için **%16 oranında** iyileşme sağlanmıştır.

## 4. Nasıl Çalıştırılır?

1.  **Gerekli Kütüphaneleri Kurun:**
    ```bash
    pip install pandas numpy matplotlib seaborn statsmodels pmdarima prophet tensorflow scikit-learn
    ```
2.  **Veri Dosyasını Hazırlayın:** Elle düzenlenmiş `MRC_Veri_Temiz.xlsx` dosyasını (Tarih, Urun_Kodu, Satis_Adedi sütunları ile) proje klasörüne yerleştirin.
3.  **Kodu Çalıştırın:** `proje_sarima.py` dosyasını çalıştırarak modelin çıktısını alabilirsiniz.
