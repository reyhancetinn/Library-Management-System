import unittest
from app import Library, Book

class TestLibrarySystem(unittest.TestCase):
    """
    Kütüphane Yönetim Sistemi - Kapsamlı Test Senaryoları
    """

    def setUp(self):
        # Her test fonksiyonundan önce çalışır ve temiz bir ortam hazırlar.
        self.lib = Library()
        self.sample_book = Book("Simyacı", "Paulo Coelho", "1988")

    # --- TEMEL FONKSİYON TESTLERİ ---

    def test_01_initial_state(self):
        # Senaryo: Kütüphane ilk oluşturulduğunda boş olmalı.
        self.assertEqual(len(self.lib.books), 0, "Hata: Yeni kütüphane boş başlamadı!")

    def test_02_add_book(self):
        # Senaryo: Kitap ekleme işlemi başarılı mı?
        self.lib.add_book(self.sample_book)
        self.assertEqual(len(self.lib.books), 1)
        self.assertEqual(self.lib.books[0].name, "Simyacı")

    def test_03_book_str_representation(self):
        # Senaryo: Book sınıfının __str__ metodu doğru formatta çıktı veriyor mu?
        expected_output = "Kitap Adı: Simyacı, Yazar: Paulo Coelho, Yayın Yılı: 1988"
        self.assertEqual(str(self.sample_book), expected_output)

    # --- ARAMA TESTLERİ ---

    def test_04_search_case_insensitive(self):
        # Senaryo: Küçük harfle arama yapıldığında büyük harfli kayıt bulunuyor mu?
        self.lib.add_book(self.sample_book)
        results = self.lib.search_by_name("simyacı")  # Küçük harf
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0].name, "Simyacı")

    def test_05_search_by_author(self):
        # Senaryo: Yazarın isminin bir kısmıyla arama yapılabiliyor mu?
        self.lib.add_book(self.sample_book)
        results = self.lib.search_by_author("Coelho")
        self.assertTrue(len(results) > 0)

    def test_06_search_not_found(self):
        # Senaryo: Olmayan bir kitap arandığında liste boş mu dönüyor?
        self.lib.add_book(self.sample_book)
        results = self.lib.search_by_name("Harry Potter")
        self.assertEqual(len(results), 0)

    # --- SİLME VE SINIR DURUM TESTLERİ ---

    def test_07_remove_existing_book(self):
        # Senaryo: Var olan bir kitabı silme.
        self.lib.add_book(self.sample_book)
        result = self.lib.remove_book("Simyacı")
        self.assertTrue(result) # True dönmeli
        self.assertEqual(len(self.lib.books), 0) # Liste boşalmalı

    def test_08_remove_non_existent_book(self):
        # Senaryo: Listede OLMAYAN bir kitabı silmeye çalışırsak ne olur?
        # Sistem hata vermemeli, sadece False döndürmeli.
        self.lib.add_book(self.sample_book)
        result = self.lib.remove_book("Olmayan Kitap")
        self.assertFalse(result, "Hata: Olmayan kitap silinmiş gibi işlem yapıldı!")
        self.assertEqual(len(self.lib.books), 1, "Hata: Silinmemesi gereken kitap silindi!")

if __name__ == '__main__':
    unittest.main()