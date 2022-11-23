from classes import Page
import sqlite3

conn = sqlite3.connect("reviews.db")

cursor = conn.cursor()
with open('create_database.sql', 'r') as f:
    cursor.execute(f.read())
cursor.close()

URL = 'https://uk.trustpilot.com/review/inpost.co.uk?languages=all&page=%s'

number_of_pages = 3000

for page_no in range(1, number_of_pages+1):
    page = Page(URL % page_no)
    for review in page.reviews:
        review.insert_into_database(connection=conn)

conn.close()