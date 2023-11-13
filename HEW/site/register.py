from flask import Flask, redirect, url_for, render_template, request
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

# /login
@app.route('/login')
def LoginPage():
    return render_template("login.html")

# /register
@app.route('/register')
def RegistrationPage():
    return render_template("registration.html")

# /register/
@app.route('/register/',methods=['POST'])
def register():
    if request.method == 'POST':
        
        # フォーム
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = conn_db()
        cursor = conn.cursor()
        
        # AccountIDの最高値を取得
        sql = "SELECT MAX(AccountID) FROM Account;"
        cursor.execute(sql)
        max_id = cursor.fetchone()[0]
        # 値がない場合は「0」
        if max_id is None:
            max_id = 0
         
        # INSERT
        sql = "INSERT INTO Account (AccountID, UserName, Password, MailAddress) VALUES ({0}, '{1}', '{2}', '{3}');".format(max_id + 1, username, password, email)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        
        return redirect(url_for("LoginPage"))

# 確認用--------------------
# @app.route('/users')
# def list_users():
#     conn = conn_db()
#     cursor = conn.cursor()
#     sql = "SELECT AccountID, UserName, MailAddress, Password FROM Account;"
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template("user_list.html", data=data)
# --------------------