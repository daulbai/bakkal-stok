import veritabani

# --- KATEGORİ İŞLEMLERİ ---

def tum_kategoriler():
    return veritabani.kategorileri_getir()

def kategori_ekle(ad):
    # Boşluk kontrolü
    if not ad or not ad.strip():
        return False, "Kategori adı boş olamaz."
    veritabani.kategori_ekle(ad.strip())
    return True, "Kategori eklendi."

def kategori_guncelle(kategori_id, yeni_ad):
    if not yeni_ad or not yeni_ad.strip():
        return False, "Kategori adı boş olamaz."
    veritabani.kategori_guncelle(kategori_id, yeni_ad.strip())
    return True, "Kategori güncellendi."

def kategori_sil(kategori_id):
    veritabani.kategori_sil(kategori_id)
    return True, "Kategori silindi."

# --- ÜRÜN İŞLEMLERİ ---

def tum_urunler():
    return veritabani.urunleri_getir()

def urun_getir(urun_id):
    return veritabani.urun_getir(urun_id)

def urun_ekle(barkod, ad, fiyat, stok, kategori_id):
    if float(fiyat) < 0:
        return False, "Fiyat negatif olamaz."
    if int(stok) < 0:
        return False, "Stok negatif olamaz."
    veritabani.urun_ekle(barkod, ad, fiyat, stok, kategori_id)
    return True, "Ürün eklendi."

def urun_guncelle(urun_id, barkod, ad, fiyat, stok, kategori_id):
    if float(fiyat) < 0:
        return False, "Fiyat negatif olamaz."
    if int(stok) < 0:
        return False, "Stok negatif olamaz."
    veritabani.urun_guncelle(urun_id, barkod, ad, fiyat, stok, kategori_id)
    return True, "Ürün güncellendi."

def urun_sil(urun_id):
    veritabani.urun_sil(urun_id)
    return True, "Ürün silindi."

# --- SATIŞ İŞLEMLERİ ---

def tum_satislar():
    return veritabani.satislari_getir()

def satis_yap(sepet):
    # Sepet boş mu?
    if not sepet:
        return False, "Sepet boş."

    # Stok kontrolü
    for item in sepet:
        urun = urun_getir(item['urun_id'])
        if not urun:
            return False, f"Ürün bulunamadı (ID: {item['urun_id']})"
        if urun['StokMiktari'] < item['miktar']:
            return False, f"Yetersiz stok: {urun['UrunAdi']} (Mevcut: {urun['StokMiktari']})"

    # Satış oluştur
    satis_id = veritabani.satis_baslat()
    if not satis_id:
        return False, "Satış oluşturulamadı."

    # Her ürünü satışa ekle (trigger stoku otomatik düşürür)
    for item in sepet:
        urun = urun_getir(item['urun_id'])
        veritabani.satis_detay_ekle(satis_id, item['urun_id'], item['miktar'], urun['Fiyat'])

    return True, "Satış tamamlandı."
