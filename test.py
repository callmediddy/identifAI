import sqlite3
from hashing import difference_hash, average_hash, hamming_distance
from PIL import Image
import os

conn = sqlite3.connect("app.db")
cur = conn.cursor()
cur.execute("SELECT username, dhash from imagedata")
x = cur.fetchall()
for i in range(len(x)):
  print(x[i][0], x[i][1])
conn.close()