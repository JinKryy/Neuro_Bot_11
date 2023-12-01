import sqlite3

def minus_token(mes):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    token = int("".join(c for c in token_cortege if c.isalnum()))  # значение токена
    token -= 1
    token = str(token)
    cur.execute(f"UPDATE users SET token = {token} WHERE id = {mes}")
    con.commit()
    cur.close()
    con.close()

def minus_gift_token(mes):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT gift_token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    gift_token = int("".join(c for c in token_cortege if c.isalnum()))  # значение токена
    if gift_token != 0:
        gift_token -= 1
        gift_token = str(gift_token)
        cur.execute(f"UPDATE users SET gift_token = {gift_token} WHERE id = {mes}")
        con.commit()
        cur.close()
        con.close()
    else:
        cur.close()
        con.close()

def plus_token(mes):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    token = int("".join(c for c in token_cortege if c.isalnum()))  # значение токена
    token += 1
    token = str(token)
    cur.execute(f"UPDATE users SET token = {token} WHERE id = {mes}")
    con.commit()
    cur.close()
    con.close()