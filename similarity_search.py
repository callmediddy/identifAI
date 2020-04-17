import sqlite3
from hashing import difference_hash, average_hash, hamming_distance
from PIL import Image

def find_similar_image(username, hashtype, img):
  dhash = difference_hash(img)
  ahash = average_hash(img)
  conn = sqlite3.connect("app.db")
  conn.execute('CREATE TABLE IF NOT EXISTS imagedata (username TEXT, dhash TEXT, ahash TEXT)')
  cur = conn.cursor()
  is_similar = False
  # This is where you can add other hashtypes if needed
  if(hashtype == 'dhash'):
    cur.execute("SELECT username, dhash from imagedata")
    x = cur.fetchall()
    # print(x)
    for i in range(len(x)):
      if(hamming_distance(dhash, x[i][1], 10)):
        if(username != x[i][0]):
          is_similar = True
          break
  else:
    cur.execute("SELECT username, ahash from imagedata")
    x = cur.fetchall()
    for i in range(len(x)):
      if(hamming_distance(ahash, x[i][1], 10)):
        if(username != x[i][0]):
          is_similar = True
          break
  if(is_similar == True):
    conn.close()
    return False
  else:
    cur.execute("INSERT INTO imagedata (username,dhash,ahash) VALUES (?,?,?)",(username,dhash,ahash))
    print("Inserted into table")
    conn.commit()
    conn.close()
    return True