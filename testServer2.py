from flask import Flask,request,jsonify,render_template,session,redirect
from datetime import timedelta
from pymongo import MongoClient
import datetime
import html

client=MongoClient("127.0.0.1", 27017)
collection_user=client["testdb"]["users"]

application = Flask(__name__)

#デフォルトルート

app = Flask(__name__)
#シークレットキー
app.secret_key="user"
#60分間セッションを維持
app.permanent_session_lifetime=timedelta(minutes=60)

@app.route("/")
def sra():
    return redirect("login")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="GET":
        res=""
        res=res+"<form method=\"POST\" action=\"login\">\n"
        res=res+"<table border=\"1\" align=\"center\">\n"
        res=res+"\t<tr><td>名前</td><td><input type=\"text\" name=\"name\"></td></tr>"
        res=res+"\t<tr><td>パスワード</td><td><input type=\"password\" name=\"pass\"></td></tr>\n"
        res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"ログイン\"></td></tr>\n"
        res=res+"</table>\n"
        res=res+"</form>"
        return res
    elif request.method=="POST":
        name=request.form["name"]
        passw=request.form["pass"]
        flag=0
        client=MongoClient("127.0.0.1", 27017)
        collection_user=client["testdb"]["users"]
        for data in collection_user.find(filter={"name":name}):
            if data["pass"]==passw:
                session["user_name"]=name
                return redirect("home")
            else:
                res=""
                res=res+"<h3>間違っています</h3>"
                res=res+"<form method=\"POST\" action=\"login\">\n"
                res=res+"<table border=\"1\" align=\"center\">\n"
                res=res+"\t<tr><td>名前</td><td><input type=\"text\" name=\"name\"></td></tr>"
                res=res+"\t<tr><td>パスワード</td><td><input type=\"password\" name=\"pass\"></td></tr>\n"
                res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"ログイン\"></td></tr>\n"
                res=res+"</table>\n"
                res=res+"</form>"
                return res

@app.route("/home",methods=["GET","POST"])
def home():
    if "user_name" in session:
        if request.method=="GET":
            client=MongoClient("127.0.0.1", 27017)
            collection_title=client["testdb"]["title"]
            res=""
            res=res+"<form method=\"POST\" action=\"home\">\n"
            res=res+"<table border=1>\n"
            res=res+"\t<tr><td>タイトル</td><td><input name=\"title\" type=\"text\"></td></tr>\n"
            res=res+"\t<tr><td>内容</td><td><textarea name=\"cont\"></textarea></form></td></tr>\n"
            res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"送信\"></td></tr>\n"
            res=res+"</table>\n"
            res=res+"</form>\n"
            res=res+"<table border=1>\n"
            for data in collection_title.find():
                res=res+"\t<tr><td>タイトル</td><td>"+html.escape(data["title"])+"</td><td>作成者</td><td>"+html.escape(data["user"])+"</td><td>作成日時</td><td>"+html.escape(data["time"])+"</td></tr>\n"
                res=res+"\t<tr><td colspan=6><pre>"+html.escape(data["cont"])+"</pre></td></tr>\n"
            res=res+"</table>"
            return res
        elif request.method=="POST":
            title=request.form["title"]
            cont=request.form["cont"]
            name=session["user_name"]
            date=str(datetime.datetime.today())[0:19]
            client=MongoClient("127.0.0.1", 27017)
            collection_title=client["testdb"]["title"]
            collection_title.insert({"title":title,"cont":cont,"user":name,"time":date})
            res=""
            res=res+"<form method=\"POST\" action=\"home\">\n"
            res=res+"<table border=1>\n"
            res=res+"\t<tr><td>タイトル</td><td><input name=\"title\" type=\"text\"></td></tr>\n"
            res=res+"\t<tr><td>内容</td><td><textarea name=\"cont\"></textarea></form></td></tr>\n"
            res=res+"\t<tr><td colspan=\"2\"><input type=\"submit\" value=\"送信\"></td></tr>\n"
            res=res+"</table>\n"
            res=res+"</form>\n"
            res=res+"<table border=1>\n"
            for data in collection_title.find():
                res=res+"\t<tr><td>タイトル</td><td>"+html.escape(data["title"])+"</td><td>作成者</td><td>"+html.escape(data["user"])+"</td><td>作成日時</td><td>"+html.escape(data["time"])+"</td></tr>\n"
                res=res+"\t<tr><td colspan=6><pre>"+html.escape(data["cont"])+"</pre></td></tr>\n"
            res=res+"</table>"
            return res

    else:
        return redirect("login")

if __name__ == "__main__":
    app.run(host="0.0.0.0")