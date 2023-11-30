from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)

# SQL
def conn_db():
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "P@ssw0rd",
        db = "hew"
    )
    return conn

# 確認用--------------------
@app.route('/index')
def IndexPage():
    return render_template("index.html")
# --------------------

# /register
@app.route('/register')
def RegistrationPage():
    return render_template("registration.html")

# /login
@app.route('/login')
def LoginPage():
    return render_template("login.html")
   
# /login/
@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        
        # フォーム
        email = request.form['email']
        password = request.form['password']
        
        # SELECT
        conn = conn_db()
        cursor = conn.cursor()
        sql = "SELECT MailAddress, Password FROM Account WHERE MailAddress = '{0}' AND Password = '{1}';".format(email, password)
        cursor.execute(sql)
        
        # 認証
        user = cursor.fetchone()
        if user:
            # 成功
            
            # ↓8行追加-出品機能のAccountID用
            get = '''
                   SELECT AccountID, UserName, MailAddress 
                   FROM Account WHERE MailAddress = '{0}' AND Password = '{1}';
                  '''.format(email, password)
            cursor.execute(get)
            you = cursor.fetchall()
            # セッションへログイン情報を保存
            session['you'] = you
            return render_template("index.html")
        else:
            # 失敗
            PassMessage = "！！メールアドレスとパスワードが一致しません！！"
            return render_template("login.html", PassMessage=PassMessage)