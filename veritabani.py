import mysql.connector
from mysql.connector import Error

# Veritabanına bağlantı kurar, hata olursa None döner
def baglan():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='BakkalDB',
            user='root',
            password=''
        )
        return conn
    except Error as e:
        print(f"Bağlantı hatası: {e}")
        return None

# Stored procedure çağırır ve sonuç döner
def prosedur_cagir(prosedur_adi, parametreler=()):
    conn = baglan()
    if not conn:
        return False
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(prosedur_adi, parametreler)
        sonuclar = []
        for sonuc in cursor.stored_results():
            sonuclar.append(sonuc.fetchall())
        conn.commit()
        return sonuclar[0] if len(sonuclar) == 1 else sonuclar
    except Error as e:
        print(f"Prosedür hatası ({prosedur_adi}): {e}")
        conn.rollback()
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- KATEGORİ İŞLEMLERİ ---

def kategorileri_getir():
    sonuc = prosedur_cagir('sp_Kategori_Listele')
    return sonuc if sonuc else []

def kategori_ekle(ad):
    return prosedur_cagir('sp_Kategori_Ekle', (ad,))

def kategori_guncelle(kategori_id, yeni_ad):
    return prosedur_cagir('sp_Kategori_Guncelle', (kategori_id, yeni_ad))

def kategori_sil(kategori_id):
    return prosedur_cagir('sp_Kategori_Sil', (kategori_id,))

# --- ÜRÜN İŞLEMLERİ ---

def urunleri_getir():
    sonuc = prosedur_cagir('sp_Urun_Listele')
    return sonuc if sonuc else []

def urun_getir(urun_id):
    sonuc = prosedur_cagir('sp_Urun_Getir', (urun_id,))
    return sonuc[0] if sonuc and len(sonuc) > 0 else None

def urun_ekle(barkod, ad, fiyat, stok, kategori_id):
    return prosedur_cagir('sp_Urun_Ekle', (barkod, ad, fiyat, stok, kategori_id))

def urun_guncelle(urun_id, barkod, ad, fiyat, stok, kategori_id):
    return prosedur_cagir('sp_Urun_Guncelle', (urun_id, barkod, ad, fiyat, stok, kategori_id))

def urun_sil(urun_id):
    return prosedur_cagir('sp_Urun_Sil', (urun_id,))

# --- SATIŞ İŞLEMLERİ ---

def satislari_getir():
    sonuc = prosedur_cagir('sp_Satis_Listele')
    return sonuc if sonuc else []

def satis_baslat():
    # OUT parametresi olan prosedür ayrı işleniyor
    conn = baglan()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        args = [0]
        donenler = cursor.callproc('sp_Satis_Baslat', args)
        conn.commit()
        return donenler[0]  # yeni satis_id
    except Error as e:
        print(f"Satış başlatma hatası: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return None

def satis_detay_ekle(satis_id, urun_id, miktar, birim_fiyat):
    return prosedur_cagir('sp_Satis_Detay_Ekle', (satis_id, urun_id, miktar, birim_fiyat))
