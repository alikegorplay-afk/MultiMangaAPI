from pageparser import MangaSearch
from magaparser import parse_from_url
import sqlite3
import logging

logger = logging.Logger(__name__)

finder = MangaSearch.default_find()
last_result = True

db = sqlite3.connect('db.db')
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS manga (
        title STRING,
        url STRING,
        poster STRING,
        gallery STRING,
        genres STRING,
        author STRING,
        language STRING
    )               
""")

while last_result is not None:
    last_result = finder.next_page()
    for manga in last_result:
        a = tuple([x if isinstance(x, str) else ','.join(x) for x in parse_from_url(manga.url).__dict__.values()])
        cursor.execute("""
            INSERT INTO manga VALUES (?, ?, ?, ?, ?, ?, ?)      
        """, a)
    db.commit()
cursor.close()
db.close()