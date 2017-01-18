import sqlite3

conn = sqlite3.connect('biocaddie.db')

with conn:
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE itemScore(id INTEGER, titleScore REAL, titleCount INTEGER, keywordsScore REAL, keyWordCount INTEGER, descriptionScore REAL, descriptionCount INTEGER, FOREIGN KEY(id) REFERENCES common(id))")