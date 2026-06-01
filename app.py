from flask import Flask, render_template, request, redirect, url_for, flash
import is_katmani

app = Flask(__name__)
app.secret_key = 'bakkal-gizli-anahtar-2024'

# Ana sayfa - ürün listesi
@app.route('/')
def ana_sayfa():
    urunler = is_katmani.tum_urunler()
    return render_template('urun_listesi.html', urunler=urunler)

# --- KATEGORİ ROUTE'LARI ---

@app.route('/kategoriler', methods=['GET', 'POST'])
def kategoriler():
    if request.method == 'POST':
        ad = request.form.get('kategori_adi')
        basarili, mesaj = is_katmani.kategori_ekle(ad)
        flash(mesaj, 'success' if basarili else 'danger')
        return redirect(url_for('kategoriler'))
    kategoriler = is_katmani.tum_kategoriler()
    return render_template('kategori_listesi.html', kategoriler=kategoriler)

@app.route('/kategori/duzenle/<int:kategori_id>', methods=['GET', 'POST'])
def kategori_duzenle(kategori_id):
    kategoriler = is_katmani.tum_kategoriler()
    kategori = next((k for k in kategoriler if k['KategoriID'] == kategori_id), None)
    if not kategori:
        flash('Kategori bulunamadı.', 'danger')
        return redirect(url_for('kategoriler'))
    if request.method == 'POST':
        yeni_ad = request.form.get('kategori_adi')
        basarili, mesaj = is_katmani.kategori_guncelle(kategori_id, yeni_ad)
        flash(mesaj, 'success' if basarili else 'danger')
        return redirect(url_for('kategoriler'))
    return render_template('kategori_duzenle.html', kategori=kategori)

@app.route('/kategori/sil/<int:kategori_id>')
def kategori_sil(kategori_id):
    basarili, mesaj = is_katmani.kategori_sil(kategori_id)
    flash(mesaj, 'success' if basarili else 'danger')
    return redirect(url_for('kategoriler'))

# --- ÜRÜN ROUTE'LARI ---

@app.route('/urun/ekle', methods=['GET', 'POST'])
def urun_ekle():
    if request.method == 'POST':
        barkod = request.form.get('barkod')
        ad = request.form.get('ad')
        fiyat = request.form.get('fiyat')
        stok = request.form.get('stok')
        kategori_id = request.form.get('kategori_id')
        basarili, mesaj = is_katmani.urun_ekle(barkod, ad, fiyat, stok, kategori_id)
        flash(mesaj, 'success' if basarili else 'danger')
        if basarili:
            return redirect(url_for('ana_sayfa'))
    kategoriler = is_katmani.tum_kategoriler()
    return render_template('urun_ekle.html', kategoriler=kategoriler)

@app.route('/urun/duzenle/<int:urun_id>', methods=['GET', 'POST'])
def urun_duzenle(urun_id):
    urun = is_katmani.urun_getir(urun_id)
    if not urun:
        flash('Ürün bulunamadı.', 'danger')
        return redirect(url_for('ana_sayfa'))
    if request.method == 'POST':
        barkod = request.form.get('barkod')
        ad = request.form.get('ad')
        fiyat = request.form.get('fiyat')
        stok = request.form.get('stok')
        kategori_id = request.form.get('kategori_id')
        basarili, mesaj = is_katmani.urun_guncelle(urun_id, barkod, ad, fiyat, stok, kategori_id)
        flash(mesaj, 'success' if basarili else 'danger')
        if basarili:
            return redirect(url_for('ana_sayfa'))
    kategoriler = is_katmani.tum_kategoriler()
    return render_template('urun_duzenle.html', urun=urun, kategoriler=kategoriler)

@app.route('/urun/sil/<int:urun_id>')
def urun_sil(urun_id):
    basarili, mesaj = is_katmani.urun_sil(urun_id)
    flash(mesaj, 'success' if basarili else 'danger')
    return redirect(url_for('ana_sayfa'))

# --- SATIŞ ROUTE'LARI ---

@app.route('/satis', methods=['GET', 'POST'])
def satis_yap():
    if request.method == 'POST':
        urun_id = int(request.form.get('urun_id'))
        miktar = int(request.form.get('miktar'))
        sepet = [{'urun_id': urun_id, 'miktar': miktar}]
        basarili, mesaj = is_katmani.satis_yap(sepet)
        flash(mesaj, 'success' if basarili else 'danger')
        return redirect(url_for('satis_gecmisi'))
    urunler = is_katmani.tum_urunler()
    return render_template('satis_yap.html', urunler=urunler)

@app.route('/satis/gecmis')
def satis_gecmisi():
    satislar = is_katmani.tum_satislar()
    return render_template('satis_gecmisi.html', satislar=satislar)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
