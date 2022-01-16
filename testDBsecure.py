import sqlite3 as sql

dbname="test.db"
conn=sql.connect(dbname)
cur=conn.cursor()

#cur.execute("CREATE TABLE users(user_id integer primary key autoincrement,user_name text NOT NULL,email text NOT NULL,pass text NOT NULL,location text NOT NULL,tel text NOT NULL)")
#cur.execute("CREATE TABLE com(com_id integer primary key autoincrement,user_id integer NOT NULL,cont text NOT NULL)")
#cur.execute("CREATE TABLE bank(bank_id integer primary key autoincrement,user_id integer NOT NULL,det_num text NOT NULL,money integer NOT NULL)")

#cur.execute("DELETE FROM com WHERE com_id=4")
cur.execute("SELECT * FROM users")
for col in cur:
    print(col)
conn.commit()
conn.close()