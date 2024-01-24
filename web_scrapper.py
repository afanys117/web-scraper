import requests
from bs4 import BeautifulSoup
import sqlite3

def create_table():
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT
        )
    ''')

    connection.commit()
    connection.close()

def scrape_and_store_quotes():
    url = 'http://quotes.toscrape.com'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')

        connection = sqlite3.connect('quotes.db')
        cursor = connection.cursor()

        for quote, author in zip(quotes, authors):
            text = quote.get_text()
            author_name = author.get_text()

            # Insert into the database
            cursor.execute('INSERT INTO quotes (text, author) VALUES (?, ?)', (text, author_name))

        connection.commit()
        connection.close()

        print("Quotes scraped and stored successfully.")
    else:
        print("Failed to fetch quotes. Status code:", response.status_code)

def view_quotes():
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM quotes')
    quotes = cursor.fetchall()

    connection.close()

    if quotes:
        print("Quotes in the database:")
        for quote in quotes:
            print(f"ID: {quote[0]}, Text: {quote[1]}, Author: {quote[2]}")
    else:
        print("No quotes found in the database.")

if __name__ == "__main__":
    create_table()
    scrape_and_store_quotes()
    view_quotes()
