import pymysql

#接続情報
dbh = pymysql.connect(
         host='localhost',
         user='webuser',
         password='pAss#Word1234',
         db='testdb',
         charset='utf8',
         cursorclass=pymysql.cursors.DictCursor
    )

#カーソル
stmt = dbh.cursor()

#SQL
sql = "select * from auth_user"

#実行
stmt.execute(sql)

#取得
rows = stmt.fetchall()

#ループ
for row in rows:
    print(row)

#掃除
stmt.close();
dbh.close();