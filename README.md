# Bakkal Stok ve Satış Takip Sistemi

Küçük bir bakkalın ürünlerini, kategorilerini ve satışlarını yönetmek için yazılmış bir web uygulaması.

## Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Web Framework | Flask (Python) |
| Veritabanı | MySQL |
| UI | Bootstrap 5 |
| DB Erişimi | mysql-connector-python |

## Proje Yapısı

```
bakkal-stok/
├── app.py              # Flask uygulama - route'lar burada
├── is_katmani.py       # İş mantığı - doğrulama ve iş kuralları
├── veritabani.py       # Veri erişim katmanı - stored procedure çağrıları
├── bakkal_db.sql       # Veritabanı kurulum scripti
├── requirements.txt    # Python bağımlılıkları
└── templates/
    ├── ana_sablon.html       # Temel HTML şablonu
    ├── urun_listesi.html     # Ürün listeleme
    ├── urun_ekle.html        # Ürün ekleme formu
    ├── urun_duzenle.html     # Ürün düzenleme formu
    ├── kategori_listesi.html # Kategori listeleme ve ekleme
    ├── kategori_duzenle.html # Kategori düzenleme formu
    ├── satis_yap.html        # Satış yapma formu
    └── satis_gecmisi.html    # Satış geçmişi
```

## Kurulum

### 1. Gereksinimler
- Python 3.9+
- MySQL 8.0+

### 2. Projeyi İndir

```bash
git clone https://github.com/kullanici_adi/bakkal-stok.git
cd bakkal-stok
```

### 3. Sanal Ortam Oluştur ve Bağımlılıkları Yükle

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> ⚠️ PowerShell'de hata alırsanız şunu çalıştırın:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Veritabanını Kur

**Mac / Linux:**
```bash
mysql -u root -p < bakkal_db.sql
```

**Windows (CMD):**
```cmd
mysql -u root -p < bakkal_db.sql
```

> Veya MySQL Workbench üzerinden `bakkal_db.sql` dosyasını import edebilirsiniz:
> `File → Open SQL Script → bakkal_db.sql → Execute`

### 5. Bağlantı Ayarları

`veritabani.py` dosyasındaki bağlantı bilgilerini kendi ortamına göre düzenle:

```python
conn = mysql.connector.connect(
    host='localhost',
    database='BakkalDB',
    user='root',
    password='şifreniz'   # <-- buraya MySQL şifrenizi yazın
)
```

### 6. Uygulamayı Başlat

**Mac / Linux:**
```bash
python3 app.py
```

**Windows:**
```cmd
python app.py
```

Tarayıcıda aç: **http://localhost:3000**

---

## Özellikler

- ✅ Ürün ekleme, düzenleme, silme
- ✅ Kategori ekleme, düzenleme, silme
- ✅ Satış yapma (stok otomatik düşer — trigger ile)
- ✅ Satış geçmişini görüntüleme
- ✅ KDV'li fiyat hesaplama (function ile)
- ✅ Stok değişim logu (trigger ile)
- ✅ Tüm DB işlemleri Stored Procedure üzerinden (N-Katmanlı mimari)

## Mimari

```
Kullanıcı (Browser)
     ↓
app.py  (Presentation Layer)
     ↓
is_katmani.py  (Business Logic Layer)
     ↓
veritabani.py  (Data Access Layer)
     ↓
MySQL - Stored Procedures
```
