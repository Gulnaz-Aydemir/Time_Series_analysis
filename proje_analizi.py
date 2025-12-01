# --- FAZ 1: GEREKLİ KÜTÜPHANELERİ ÇAĞIRMA ---
# Projemizin "araç kutusunu" yüklüyoruz.
import pandas as pd                 # Veri işleme ve okuma için (Excel'i okuyacak)
import matplotlib.pyplot as plt     # Temel grafikler için
import seaborn as sns               # Daha güzel grafikler için
from statsmodels.tsa.seasonal import seasonal_decompose
# Grafiklerin daha güzel görünmesi için bazı ayarlar
sns.set_style("whitegrid")                       # Grafiklerin arka planı beyaz ve ızgaralı olsun
plt.rcParams['figure.figsize'] = (15, 8)         # Oluşacak grafiklerin boyutu büyük olsun
plt.rcParams['font.size'] = 12                   # Yazı tipi boyutu okunaklı olsun

print("--- Kütüphaneler başarıyla yüklendi. ---")


# --- FAZ 2: VERİYİ TEMİZLEME VE DÖNÜŞTÜRME (Adım 1.3'ün Otomasyonu) ---

# Dosya adını bir değişkene atayalım
EXCEL_DOSYASI = 'MRC_Veri_Temiz.xlsx'

try:
    # 1. Excel'i Oku: 'Temiz_Veri' sayfasını oku
    df = pd.read_excel(EXCEL_DOSYASI, sheet_name='Temiz_Veri')
    
    # 2. Tarihi Dönüştür: Python'a 'Tarih' sütununun metin değil, gerçek tarih olduğunu öğret
    df['Tarih'] = pd.to_datetime(df['Tarih'])
    
    # 3. İndeks Ayarla: Zaman serisi analizleri için 'Tarih' sütununu anahtar (indeks) yap
    df.set_index('Tarih', inplace=True)
    
    # 4. Ürünlere Ayır: 3 ürünü ayrı ayrı analiz edebilmek için 3 farklı değişkene ata
    df_7kw = df[df['Urun_Kodu'] == '7.5KW']['Satis_Adedi']
    df_5kw = df[df['Urun_Kodu'] == '5.5KW']['Satis_Adedi']
    df_11kw = df[df['Urun_Kodu'] == '11KW']['Satis_Adedi']

    print(f"--- '{EXCEL_DOSYASI}' başarıyla okundu ve işlendi. ---")
    print("Veri özeti (ilk 5 satır):")
    print(df.head())

except FileNotFoundError:
    print(f"HATA: '{EXCEL_DOSYASI}' dosyası bulunamadı!")
    print(f"Lütfen '{EXCEL_DOSYASI}' dosyasının bu Python dosyasıyla aynı klasörde olduğundan emin ol.")
except Exception as e:
    print(f"Bir hata oluştu: {e}")


# --- FAZ 3: KEŞİFSEL VERİ ANALİZİ (EDA) - (İlk "Güzel Çıktıları" Alma) ---

# ÇIKTI 1: Tüm Ürünlerin Zaman Serisi Grafiği
# ------------------------------------------------
print("\nÇIKTI 1: Tüm ürünlerin zaman serisi grafiği oluşturuluyor...")
plt.figure(figsize=(15, 8)) # Bu grafik için yeni bir pencere aç
plt.plot(df_7kw.index, df_7kw, label='7.5KW Kumanda Sistemi', marker='o', linestyle='-')
plt.plot(df_5kw.index, df_5kw, label='5.5KW Kumanda Sistemi', marker='s', linestyle='--')
plt.plot(df_11kw.index, df_11kw, label='11KW Kumanda Sistemi', marker='^', linestyle=':')

# Grafiğe başlık ve etiket ekle
plt.title('MRC Asansör Ürün Satışları Zaman Serisi', fontsize=16)
plt.ylabel('Haftalık Satış Adedi')
plt.xlabel('Tarih')
plt.legend() # Hangi çizginin hangi ürüne ait olduğunu gösteren kutu
plt.grid(True)

# Grafiği raporun için resim dosyası olarak kaydet
plt.savefig('CIKTI_1_Tum_Urunler_Zaman_Serisi.png')
print("Grafik 'CIKTI_1_Tum_Urunler_Zaman_Serisi.png' olarak kaydedildi.")


# ÇIKTI 2: Bileşenlere Ayırma Grafiği (En Önemli Ürün için)
# ------------------------------------------------
print("\nÇIKTI 2: 7.5KW ürünü için bileşenler grafiği oluşturuluyor...")
# NOT: Veri setimiz 1 yıllık (24 dönem)  olduğu için, 'period=12' (6 aylık bir desen) aramak mantıklı.
# Eğer 3-4 yıllık AYLIK veri alsaydık burayı 'period=12' (yıllık desen) yapacaktık.
# Eğer 3-4 yıllık HAFTALIK veri alsaydık 'period=52' yapacaktık.
try:
    # 7.5KW ürününün verisini al ve bileşenlerine (Trend, Mevsimsellik, Gürültü) ayır
    decomposition = seasonal_decompose(df_7kw, model='additive', period=12) # 6 aylık periyot varsayıyoruz
    
    # Bu bileşenleri çizdir
    fig = decomposition.plot()
    fig.set_size_inches(12, 10)
    plt.suptitle('CIKTI 2: 7.5KW Ürünü - Bileşenler (Trend, Mevsimsellik, Artık)', y=1.03)
    
    # Bu grafiği de kaydet
    plt.savefig('CIKTI_2_7.5KW_Bilesenler.png')
    print("Grafik 'CIKTI_2_7.5KW_Bilesenler.png' olarak kaydedildi.")

except ValueError as e:
    # Bu hata genelde 'period' değeri veri sayısından büyükse veya veri çok azsa çıkar
    print(f"Bileşenlere ayırma hatası (Veri azlığından olabilir): {e}")


# ÇIKTI 3: Aylık Ortalama Satışlar (Mevsimsellik Kanıtı)
# ------------------------------------------------
print("\nÇIKTI 3: Aylık ortalama satış grafiği oluşturuluyor...")
df_kopya = df.reset_index() # Tarih indeksini normale çevir
df_kopya['Ay'] = df_kopya['Tarih'].dt.month_name() # Tarihten 'Ocak', 'Şubat' gibi ay isimleri çıkar
aylar_sirali = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]

plt.figure(figsize=(15, 7))
# 'Urun_Kodu'na göre kırılım yaparak (hue) aylık ortalamaları çiz
sns.barplot(
    data=df_kopya, 
    x='Ay', 
    y='Satis_Adedi', 
    hue='Urun_Kodu', 
    order=aylar_sirali # Ayları doğru sırada (Ocak, Şubat...) göster
)
plt.title('CIKTI 3: Ürün Bazlı Aylık Ortalama Satışlar (Mevsimsellik Analizi)')
plt.ylabel('Ortalama Satış Adedi')
plt.xlabel('Aylar')
plt.savefig('CIKTI_3_Aylik_Ortalama_Satislar.png')
print("Grafik 'CIKTI_3_Aylik_Ortalama_Satislar.png' olarak kaydedildi.")


# --- FAZ 4: GRAFİKLERİ GÖSTERME ---
print("\n--- Analiz Tamamlandı. Tüm grafikler şimdi ekranda gösterilecek. ---")
plt.show() # Üretilen tüm grafikleri ekranda açarsss