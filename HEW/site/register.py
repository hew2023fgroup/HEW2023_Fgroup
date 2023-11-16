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
        
        # 既に登録されているメールアドレス
        sql = "SELECT * FROM Account WHERE MailAddress='{0}'".format(email)
        cursor.execute(sql)
        existing_user = cursor.fetchone()

        if existing_user:
            MailMessage = "！！既に登録されたアドレスです！！"
            return render_template("registration.html", MailMessage=MailMessage)

        # メールアドレスが登録されていない場合
        # INSERT
        sql = "INSERT INTO Account (UserName, Password, MailAddress) VALUES ('{0}', '{1}', '{2}');".format(username, password, email)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        
        return render_template("login.html")
    
# アカウント作成確認用------------------------------------------------------------
# @app.route('/users')
# def list_users():
#     conn = conn_db()
#     cursor = conn.cursor()
#     sql = "SELECT AccountID, UserName, MailAddress, Password FROM Account;"
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template("user_list.html", data=data)
# ------------------------------------------------------------

# /usersで確認&削除用------------------------------------------------------------
# @app.route("/delete/", methods=["GET"])
# def user_delete():
#     conn = ""
#     cursor = ""
#     try:
#         id = request.args.get("id")
#         conn = conn_db()
#         cursor = conn.cursor()
#         sql = "delete from Account where AccountID = {0}".format(id)
#         cursor.execute(sql)
#         conn.commit()
#     except mysql.connector.ProgrammingError as e:
#         print(e)
#     finally:
#         if cursor !="":
#             cursor.close()
#         if conn.connection_id !="":
#             conn.close()
#     return  redirect(url_for("list_users"))
# ------------------------------------------------------------