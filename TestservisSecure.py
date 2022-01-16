from flask import Flask,request,jsonify,render_template,session,redirect
from datetime import timedelta
import sqlite3 as sql

app = Flask(__name__)
#シークレットキー
app.secret_key="user"
#60分間セッションを維持
app.permanent_session_lifetime=timedelta(minutes=60)

@app.route("/")
def sra():
    return redirect("login")

@app.route("/newac",methods=["GET","POST"])
def newac():
    if request.method=="GET":
        res="<form action=\"newac\" method=\"POST\">\n<table border=\"1\">"
        res=res+"\t<tr><td>名前</td><td><input type=\"text\" name=\"user_name\"></td></tr>"
        res=res+"\t<tr><td>住所</td><td><input type=\"text\" name=\"location\"></td></tr>"
        res=res+"\t<tr><td>電話番号</td><td><input type=\"text\" name=\"tel\"></td></tr>"
        res=res+"\t<tr><td>パスワード</td><td><input type=\"password\" name=\"pass\"></td></tr>"
        res=res+"\t<tr><td>メールアドレス</td><td><input type=\"text\" name=\"email\"></td></tr>"
        res=res+"\t<tr><td colspan=\"2\" align=\"right\"><input type=\"submit\" value=\"送信\"></td></tr>"
        res=res+"</form>\n</table>"
        return res
    elif request.method=="POST":
        user_name=request.form["user_name"]
        location=request.form["location"]
        tel=request.form["tel"]
        passw=request.form["pass"]
        email=request.form["email"]
        dbname="test.db"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("INSERT INTO users (user_name,pass,email,location,tel) VALUES ('%s','%s','%s','%s','%s')"%(user_name,passw,email,location,tel))
        conn.commit()
        conn.close()
        return redirect("/login")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        res="<a href=\"newac\">新規登録</a><br>\n<table border=\"1\" align=\"center\">\n"
        res=res+"<form method=\"POST\" action=\"login\">\n"
        res=res+"\t<tr><td align=\"center\">メールアドレス</td><td><input type=\"text\" name=\"email\"></td></tr>\n"
        res=res+"\t<tr><td align=\"center\">パスワード</td><td><input type=\"password\" name=\"pass\"></td></tr>\n"
        res=res+"\t<tr><td colspan=\"2\" align=\"right\"><input type=\"submit\" value=\"送信\"></td></tr>"
        res=res+"</form>\n</table>"
        return res
    elif request.method=="POST":
        email=request.form["email"]
        passw=request.form["pass"]
        dbname="test.db"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("SELECT user_id,user_name FROM users WHERE pass='%s' AND email='%s'"%(passw,email))
        tmp=[]
        for col in cur:
            tmp.append(col[1])
            session["user_id"]=col[0]
        conn.close()
        if len(tmp)!=0:
            print(email)
            print(tmp[0])
            #session.permanent = True
            session["user_name"]=tmp[0]
            return redirect("/home")
        else:
            res="<h3>間違っています</h3><a href=\"newac\">新規登録</a><br>\n<table border=\"1\" align=\"center\">\n"
            res=res+"<form method=\"POST\" action=\"login\">\n"
            res=res+"\t<tr><td align=\"center\">メールアドレス</td><td><input type=\"text\" name=\"email\"></td></tr>\n"
            res=res+"\t<tr><td align=\"center\">パスワード</td><td><input type=\"password\" name=\"pass\"></td></tr>\n"
            res=res+"\t<tr><td colspan=\"2\" align=\"right\"><input type=\"submit\" value=\"送信\"></td></tr>"
            res=res+"</form>\n</table>"
            return res

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="GET":
        print(session)
        user_name=session["user_name"]
        dbname="test.db"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("SELECT user_name,location,tel,email FROM users WHERE user_name='%s'"%(user_name))
        res="<table border=\"1\">"
        for col in cur:
            res=res+"\t<tr><td>名前</td><td>%s</td></tr>"%(col[0])
            res=res+"\t<tr><td>住所</td><td>%s</td></tr>"%(col[1])
            res=res+"\t<tr><td>電話番号</td><td>%s</td></tr>"%(col[2])
            res=res+"\t<tr><td>メールアドレス</td><td>%s</td></tr>"%(col[3])
        conn.close()
        res=res+"</table>\n"
        res=res+"<form method=\"POST\" action=\"csrftest\">"
        res=res+"<h2>送金先口座番号と金額を入力してください</h2>"
        res=res+"<table border=1>\n"
        res=res+"\t<tr><td>送金先口座番号</td><td><input type=\"text\" name=\"det\"></td></tr>\n"
        res=res+"\t<tr><td>金額</td><td><input type=\"text\" name=\"money\"></td></tr>\n"
        res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"送金\"></td></tr>\n"
        res=res+"</table>\n</form>"
        res=res+"<form method=\"POST\" action=\"home\"><textarea name=cont></textarea><input type=\"submit\" value=\"送信\"></form>"
        res=res+"<table>\n"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("SELECT user_id,cont FROM com")
        for col in cur:
            cur2=conn.cursor()
            cur2.execute("SELECT user_name FROM users WHERE user_id=%d"%(col[0]))
            for col2 in cur2:
                res=res+"\t<tr><td>"+str(col2[0])+"</td><td><pre>"+str(col[1])+"</pre></td></tr>\n"
        res=res+"</table>"
        return res
    elif request.method=="POST":
        user_name=session["user_name"]
        cont=request.form["cont"]
        user_id=session["user_id"]
        dbname="test.db"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("INSERT INTO com (user_id,cont) VALUES (%d,'%s')"%(user_id,cont))
        conn.commit()
        conn.close()
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("SELECT user_name,location,tel,email FROM users WHERE user_name='%s'"%(user_name))
        res="<table border=\"1\">"
        for col in cur:
            res=res+"\t<tr><td>名前</td><td>%s</td></tr>"%(col[0])
            res=res+"\t<tr><td>住所</td><td>%s</td></tr>"%(col[1])
            res=res+"\t<tr><td>電話番号</td><td>%s</td></tr>"%(col[2])
            res=res+"\t<tr><td>メールアドレス</td><td>%s</td></tr>"%(col[3])
        conn.close()
        res=res+"</table>\n"
        res=res+"<form method=\"POST\" action=\"csrftest\">"
        res=res+"<h2>送金先口座番号と金額を入力してください</h2>"
        res=res+"<table border=1>\n"
        res=res+"\t<tr><td>送金先口座番号</td><td><input type=\"text\" name=\"det\"></td></tr>\n"
        res=res+"\t<tr><td>金額</td><td><input type=\"text\" name=\"money\"></td></tr>\n"
        res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"送金\"></td></tr>\n"
        res=res+"</table>\n</form>"
        res=res+"<form method=\"POST\" action=\"home\"><textarea name=cont></textarea><input type=\"submit\" value=\"送信\"></form>"
        res=res+"<table>\n"
        conn=sql.connect(dbname)
        cur=conn.cursor()
        cur.execute("SELECT user_id,cont FROM com")
        for col in cur:
            cur2=conn.cursor()
            cur2.execute("SELECT user_name FROM users WHERE user_id=%d"%(col[0]))
            for col2 in cur2:
                res=res+"\t<tr><td>"+str(col2[0])+"</td><td><pre>"+str(col[1])+"</pre></td></tr>\n"
        res=res+"</table>"
        return res

@app.route("/red-session",methods=["GET","POST"])
def red_session():
    if request.method=="GET":
        sid=str(request.args.get("id"))
        res="<h1>SessionKey:"+sid+"</h1>"
        return res

@app.route("/csrftest",methods=["GET","POST"])
def csrftest():
    if "user_id" in session:
        if request.method=="POST":
            det=request.form["det"]
            money=request.form["money"]
            dbname="test.db"
            conn=sql.connect(dbname)
            cur=conn.cursor()
            cur.execute("INSERT INTO bank (user_id,det_num,money) VALUES (?,?,?)",(session["user_id"],det,int(money)))
            conn.commit()
            conn.close()
            res=session["user_name"]+"様、<br>\n"
            res=res+"口座番号"+det+"へ<br>\n"
            res=res+str(money)+"円送金しました<br>\n"
            res=res+"<a href=\"home\">ホームに戻る</a>"
            return res
        else:
            print("GET")
            return redirect("home")
    else:
        print(session["user_id"])
        return redirect("home")

if __name__ == "__main__":
    app.run(host="0.0.0.0")