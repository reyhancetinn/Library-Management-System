from flask import Flask, render_template, request, redirect, url_for

import sqlite3
from db import init_db, get_connection


app = Flask(__name__)

class Book:
    """
    Kitap sınıfı: Kitapla ilgili isim, yazar ve yıl bilgilerini tutar
    """
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year

    def __str__(self):
        # Kitap bilgilerini yazdırmak için 
        return f"Kitap Adı: {self.name}, Yazar: {self.author}, Yayın Yılı: {self.year}"

class Library:
    """
    Kütüphane sınıfı: Kitap ekleme, silme, arama ve listeleme işlemlerini yönetir.
    """
    def __init__(self):
        # Kitaplar self.books listesinde tutulur 
        init_db()

    def add_book(self, book):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (name, author, year) VALUES (?, ?, ?)",
                (book.name, book.author, book.year)
        )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False




    def remove_book(self, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM books WHERE LOWER(name) = LOWER(?)",
             (name,)
    )
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        return deleted > 0


    def search_by_name(self, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, author, year FROM books WHERE name LIKE ?",
            (f"%{name}%",)
    )
        rows = cursor.fetchall()
        conn.close()
        return rows


    def search_by_author(self, author):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, author, year FROM books WHERE author LIKE ?",
            (f"%{author}%",)
    )
        rows = cursor.fetchall()
        conn.close()
        return rows


    def list_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, author, year FROM books")
        rows = cursor.fetchall()
        conn.close()
        return rows


# Kütüphane nesnesini oluşturuyor
my_library = Library()

# BÖLÜM 2: FLASK WEB ARAYÜZÜ 

@app.route('/')
def index():
    # Ana Sayfa Menüsü
    return render_template('index.html')

@app.route('/list')
def list_books():
    # Tüm kitapları listeleme sayfası 
    books = my_library.list_books()
    return render_template('list.html', books=books, title="Tüm Kitaplar")

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        year = int(request.form['year'])
        
        new_book = Book(name, author, year)
        success = my_library.add_book(new_book)

        if not success:
            return render_template(
                'add.html',
                error="Bu kitap zaten kütüphanede mevcut!"
            )

        return redirect(url_for('list_books'))

    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_book():
    # Kitap Silme Sayfası 
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        success = my_library.remove_book(name)
        if success:
            message = f"'{name}' başarıyla silindi."
        else:
            message = f"Hata: '{name}' isimli kitap bulunamadı."
    return render_template('delete.html', message=message)

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    # Arama Sayfası (Hem İsim Hem Yazar) 
    results = None
    search_type = None
    query = None
    
    if request.method == 'POST':
        query = request.form['query']
        search_type = request.form['type']
        
        if search_type == 'name':
            results = my_library.search_by_name(query)
        elif search_type == 'author':
            results = my_library.search_by_author(query)
            
    return render_template('list.html', books=results, title="Arama Sonuçları", query=query)

if __name__ == '__main__':
    app.run(debug=True)