import time
import sqlite3
from db import get_connection, init_db


# 1. Kitap Sınıfı (AYNI – değişmedi)
class Kitap:
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year

    def __str__(self):
        return f"Kitap Adı: {self.name}, Yazar: {self.author}, Yayın Yılı: {self.year}"


# 2. Library Sınıfı (SQLite KULLANAN HALİ)
class Library:
    def __init__(self):
        init_db()  # veritabanı ve tabloyu garanti altına al

    def add_book(self, book):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO books (name, author, year) VALUES (?, ?, ?)",
                (book.name, book.author, book.year)
            )
            conn.commit()
            print(f">> {book.name} başarıyla eklendi.")
        except sqlite3.IntegrityError:
            print(f">> Hata: '{book.name}' zaten kütüphanede mevcut!")
        finally:
            conn.close()

    def remove_book(self, name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM books WHERE LOWER(name) = LOWER(?)",
            (name,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            print(f">> {name} başarıyla silindi.")
        else:
            print(f">> Hata: '{name}' isimli kitap bulunamadı.")

        conn.close()

    def search_by_name(self, name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, author, year FROM books WHERE name LIKE ?",
            (f"%{name}%",)
        )
        books = cursor.fetchall()
        conn.close()

        if not books:
            print(">> Aradığınız kriterde kitap bulunamadı.")
        else:
            print(">> Arama Sonuçları:")
            for b in books:
                print(f"Kitap Adı: {b[0]}, Yazar: {b[1]}, Yayın Yılı: {b[2]}")

    def search_by_author(self, author):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, author, year FROM books WHERE author LIKE ?",
            (f"%{author}%",)
        )
        books = cursor.fetchall()
        conn.close()

        if not books:
            print(">> Bu yazara ait kayıtlı kitap bulunamadı.")
        else:
            print(f">> '{author}' yazarına ait kitaplar:")
            for b in books:
                print(f"Kitap Adı: {b[0]}, Yazar: {b[1]}, Yayın Yılı: {b[2]}")

    def list_books(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name, author, year FROM books")
        books = cursor.fetchall()
        conn.close()

        print("\n>> Kütüphanedeki Tüm Kitaplar:")
        if not books:
            print(">> Kütüphane şu an boş.")
        else:
            for b in books:
                print(f"Kitap Adı: {b[0]}, Yazar: {b[1]}, Yayın Yılı: {b[2]}")


# 3. Konsol Menü ve Ana Program
def main():
    library = Library()

    while True:
        print("\n--- Kütüphane Kitap Arama Sistemi (SQLite) ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitap Ara (İsme Göre)")
        print("4. Kitap Ara (Yazara Göre)")
        print("5. Tüm Kitapları Listele")
        print("6. Çıkış")

        choice = input("Seçiminizi yapın (1-6): ")

        if choice == '1':
            name = input("Kitap Adı: ")
            author = input("Yazar: ")
            year = input("Yayın Yılı: ")
            new_book = Kitap(name, author, year)
            library.add_book(new_book)

        elif choice == '2':
            name = input("Silinecek Kitap Adı: ")
            library.remove_book(name)

        elif choice == '3':
            name = input("Aramak istediğiniz kitabın adını girin: ")
            library.search_by_name(name)

        elif choice == '4':
            author = input("Aramak istediğiniz yazarın adını girin: ")
            library.search_by_author(author)

        elif choice == '5':
            library.list_books()

        elif choice == '6':
            print(">> Uygulamadan çıkılıyor...")
            time.sleep(1)
            break

        else:
            print(">> Geçersiz seçim, lütfen tekrar deneyin.")


# Programı Başlat
if __name__ == "__main__":
    main()

