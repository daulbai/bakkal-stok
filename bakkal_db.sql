-- BakkalDB - Bakkal Stok ve Satış Takip Sistemi
-- Veritabanı Kurulum Scripti

CREATE DATABASE IF NOT EXISTS BakkalDB CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci;
USE BakkalDB;


-- TABLOLAR

CREATE TABLE IF NOT EXISTS Kategoriler (
    KategoriID   INT          AUTO_INCREMENT PRIMARY KEY,
    KategoriAdi  VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Urunler (
    UrunID       INT           AUTO_INCREMENT PRIMARY KEY,
    Barkod       VARCHAR(50)   NOT NULL UNIQUE,
    UrunAdi      VARCHAR(100)  NOT NULL,
    Fiyat        DECIMAL(10,2) NOT NULL CHECK (Fiyat >= 0),
    StokMiktari  INT           NOT NULL DEFAULT 0 CHECK (StokMiktari >= 0),
    KategoriID   INT           NOT NULL,
    FOREIGN KEY (KategoriID) REFERENCES Kategoriler(KategoriID)
);

CREATE TABLE IF NOT EXISTS Satislar (
    SatisID      INT           AUTO_INCREMENT PRIMARY KEY,
    Tarih        DATETIME      DEFAULT CURRENT_TIMESTAMP,
    ToplamTutar  DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS Satis_Detay (
    DetayID      INT           AUTO_INCREMENT PRIMARY KEY,
    SatisID      INT           NOT NULL,
    UrunID       INT           NOT NULL,
    Miktar       INT           NOT NULL CHECK (Miktar > 0),
    BirimFiyat   DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (SatisID) REFERENCES Satislar(SatisID),
    FOREIGN KEY (UrunID)  REFERENCES Urunler(UrunID)
);

-- Stok değişikliklerini kayıt altına almak için log tablosu
CREATE TABLE IF NOT EXISTS Stok_Log (
    LogID        INT      AUTO_INCREMENT PRIMARY KEY,
    UrunID       INT      NOT NULL,
    EskiStok     INT,
    YeniStok     INT,
    IslemTarihi  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ================================================
-- ESKİ NESNELERI TEMİZLE
-- ================================================

DROP FUNCTION  IF EXISTS fn_KdvHesapla;
DROP FUNCTION  IF EXISTS fn_GunlukCiro;
DROP TRIGGER   IF EXISTS trg_Satis_Stok_Dus;
DROP TRIGGER   IF EXISTS trg_Stok_Guncelleme_Log;
DROP PROCEDURE IF EXISTS sp_Kategori_Listele;
DROP PROCEDURE IF EXISTS sp_Kategori_Ekle;
DROP PROCEDURE IF EXISTS sp_Kategori_Guncelle;
DROP PROCEDURE IF EXISTS sp_Kategori_Sil;
DROP PROCEDURE IF EXISTS sp_Urun_Listele;
DROP PROCEDURE IF EXISTS sp_Urun_Getir;
DROP PROCEDURE IF EXISTS sp_Urun_Ekle;
DROP PROCEDURE IF EXISTS sp_Urun_Guncelle;
DROP PROCEDURE IF EXISTS sp_Urun_Sil;
DROP PROCEDURE IF EXISTS sp_Satis_Baslat;
DROP PROCEDURE IF EXISTS sp_Satis_Detay_Ekle;
DROP PROCEDURE IF EXISTS sp_Satis_Listele;

-- ================================================
-- FONKSİYONLAR (en az 2 adet)
-- ================================================

DELIMITER //

-- Verilen fiyata %20 KDV ekler
CREATE FUNCTION fn_KdvHesapla(fiyat DECIMAL(10,2))
RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
    RETURN ROUND(fiyat * 1.20, 2);
END //

-- Belirli bir güne ait toplam satış cirosunu döner
CREATE FUNCTION fn_GunlukCiro(gun DATE)
RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
    DECLARE ciro DECIMAL(10,2);
    SELECT IFNULL(SUM(ToplamTutar), 0) INTO ciro
    FROM Satislar
    WHERE DATE(Tarih) = gun;
    RETURN ciro;
END //

-- ================================================
-- TETİKLEYİCİLER / TRIGGER (en az 2 adet)
-- ================================================

-- Satış detayı eklenince stoku otomatik düşürür
CREATE TRIGGER trg_Satis_Stok_Dus
AFTER INSERT ON Satis_Detay
FOR EACH ROW
BEGIN
    UPDATE Urunler
    SET StokMiktari = StokMiktari - NEW.Miktar
    WHERE UrunID = NEW.UrunID;
END //

-- Stok değişince log tablosuna kayıt atar
CREATE TRIGGER trg_Stok_Guncelleme_Log
AFTER UPDATE ON Urunler
FOR EACH ROW
BEGIN
    IF OLD.StokMiktari != NEW.StokMiktari THEN
        INSERT INTO Stok_Log (UrunID, EskiStok, YeniStok)
        VALUES (NEW.UrunID, OLD.StokMiktari, NEW.StokMiktari);
    END IF;
END //

-- ================================================
-- STORED PROCEDURE'LER - KATEGORİ
-- ================================================

CREATE PROCEDURE sp_Kategori_Listele()
BEGIN
    SELECT * FROM Kategoriler ORDER BY KategoriAdi;
END //

CREATE PROCEDURE sp_Kategori_Ekle(IN p_KategoriAdi VARCHAR(50))
BEGIN
    INSERT INTO Kategoriler (KategoriAdi) VALUES (p_KategoriAdi);
END //

CREATE PROCEDURE sp_Kategori_Guncelle(IN p_KategoriID INT, IN p_KategoriAdi VARCHAR(50))
BEGIN
    UPDATE Kategoriler SET KategoriAdi = p_KategoriAdi WHERE KategoriID = p_KategoriID;
END //

CREATE PROCEDURE sp_Kategori_Sil(IN p_KategoriID INT)
BEGIN
    DELETE FROM Kategoriler WHERE KategoriID = p_KategoriID;
END //

-- ================================================
-- STORED PROCEDURE'LER - ÜRÜN
-- ================================================

CREATE PROCEDURE sp_Urun_Listele()
BEGIN
    SELECT U.*, K.KategoriAdi, fn_KdvHesapla(U.Fiyat) AS KdvliFiyat
    FROM Urunler U
    JOIN Kategoriler K ON U.KategoriID = K.KategoriID
    ORDER BY U.UrunAdi;
END //

CREATE PROCEDURE sp_Urun_Getir(IN p_UrunID INT)
BEGIN
    SELECT U.*, K.KategoriAdi, fn_KdvHesapla(U.Fiyat) AS KdvliFiyat
    FROM Urunler U
    JOIN Kategoriler K ON U.KategoriID = K.KategoriID
    WHERE U.UrunID = p_UrunID;
END //

CREATE PROCEDURE sp_Urun_Ekle(
    IN p_Barkod      VARCHAR(50),
    IN p_UrunAdi     VARCHAR(100),
    IN p_Fiyat       DECIMAL(10,2),
    IN p_StokMiktari INT,
    IN p_KategoriID  INT
)
BEGIN
    INSERT INTO Urunler (Barkod, UrunAdi, Fiyat, StokMiktari, KategoriID)
    VALUES (p_Barkod, p_UrunAdi, p_Fiyat, p_StokMiktari, p_KategoriID);
END //

CREATE PROCEDURE sp_Urun_Guncelle(
    IN p_UrunID      INT,
    IN p_Barkod      VARCHAR(50),
    IN p_UrunAdi     VARCHAR(100),
    IN p_Fiyat       DECIMAL(10,2),
    IN p_StokMiktari INT,
    IN p_KategoriID  INT
)
BEGIN
    UPDATE Urunler
    SET Barkod = p_Barkod, UrunAdi = p_UrunAdi, Fiyat = p_Fiyat,
        StokMiktari = p_StokMiktari, KategoriID = p_KategoriID
    WHERE UrunID = p_UrunID;
END //

CREATE PROCEDURE sp_Urun_Sil(IN p_UrunID INT)
BEGIN
    DELETE FROM Urunler WHERE UrunID = p_UrunID;
END //

-- ================================================
-- STORED PROCEDURE'LER - SATIŞ
-- ================================================

CREATE PROCEDURE sp_Satis_Baslat(OUT p_SatisID INT)
BEGIN
    INSERT INTO Satislar (ToplamTutar) VALUES (0.00);
    SET p_SatisID = LAST_INSERT_ID();
END //

CREATE PROCEDURE sp_Satis_Detay_Ekle(
    IN p_SatisID    INT,
    IN p_UrunID     INT,
    IN p_Miktar     INT,
    IN p_BirimFiyat DECIMAL(10,2)
)
BEGIN
    INSERT INTO Satis_Detay (SatisID, UrunID, Miktar, BirimFiyat)
    VALUES (p_SatisID, p_UrunID, p_Miktar, p_BirimFiyat);

    -- Satışın toplam tutarını güncelle
    UPDATE Satislar
    SET ToplamTutar = ToplamTutar + (p_Miktar * p_BirimFiyat)
    WHERE SatisID = p_SatisID;
END //

CREATE PROCEDURE sp_Satis_Listele()
BEGIN
    SELECT * FROM Satislar ORDER BY Tarih DESC;
END //

DELIMITER ;