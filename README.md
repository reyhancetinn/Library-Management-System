# 📚 Kütüphane Yönetim Sistemi (Library Management System)

Bu proje, Python kullanılarak geliştirilmiş kapsamlı bir **Kütüphane Yönetim Sistemi**dir. Proje, kullanıcıların kitap eklemesine, silmesine, yazara veya kitap adına göre arama yapmasına olanak tanır. 

Veri kalıcılığı **SQLite** veritabanı ile sağlanmıştır. Projenin en güçlü yanı, aynı veritabanını kullanan iki farklı arayüze (Web ve Konsol) sahip olmasıdır.

## 🚀 Özellikler

* **Çift Arayüz:** İster terminal üzerinden (CLI), ister modern bir Web arayüzü üzerinden (Flask) kullanılabilir.
* **CRUD İşlemleri:** Kitap Ekleme, Listeleme, Silme ve Güncelleme altyapısı.
* **Gelişmiş Arama:** Kitap ismine veya yazar ismine göre filtreleme yapabilme.
* **Veritabanı:** SQLite3 ile hafif ve hızlı veri saklama.
* **Test Kapsamı:** `unittest` kütüphanesi ile yazılmış kapsamlı birim testleri (Unit Tests).

## 🛠️ Kullanılan Teknolojiler

* **Python 3.x**
* **Flask** (Web Arayüzü için)
* **SQLite3** (Veritabanı için)
* **HTML/CSS** (Web arayüzü tasarımları için)
* **Unittest** (Test senaryoları için)

## 📂 Proje Yapısı

```text
├── app.py           # Flask web uygulaması ve route yapıları
├── konsol.py        # Terminal tabanlı (CLI) kütüphane uygulaması
├── db.py            # Veritabanı bağlantı ve kurulum modülü
├── test_app.py      # Projenin birim testleri (Unit Tests)
├── library.db       # SQLite veritabanı dosyası
└── templates/       # Flask için HTML şablonları (index, add, list vb.)
