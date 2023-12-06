from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# データベース接続
def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="P@ssw0rd",
        db="hew"
    )
    return conn

#各ページへの遷移
@app.route('/index')
def IndexPage():
    return render_template("index.html")

@app.route('/managetop')
def ManagetopPage():
    return render_template("managetop.html")

@app.route('/managepage')
def ManagePage():
    return render_template("managepage.html")

@app.route('/managedb')
def ManagedbPage():
    return render_template("managedb.html")

# ユーザー情報を表示
@app.route("/manageuser")
def manageuser():
    conn = conn_db()
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM account"
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template("manageuser.html", result=result)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# 新しいユーザーをデータベースに追加
@app.route("/adduser", methods=["POST"])
def adduser():
    conn = None
    cursor = None

    try:
        username = request.form.get("username")
        email = request.form.get("email")
        # 他の情報もフォームから取得

        conn = conn_db()
        cursor = conn.cursor()
#%s:インジェクション
        sql = "INSERT INTO account (Username, Email) VALUES (%s, %s)"
        cursor.execute(sql, (username, email))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("manageuser"))

# ユーザー情報を編集
@app.route("/edituser", methods=["POST"])
def edituser():
    conn = None
    cursor = None

    try:
        user_id = request.form.get("user_id")
        new_email = request.form.get("new_email")
        # 他の情報もフォームから取得

        conn = conn_db()
        cursor = conn.cursor()

        sql = "UPDATE account SET Email=%s WHERE AccountID=%s"
        cursor.execute(sql, (new_email, user_id))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("manageuser"))

# ユーザーを削除
@app.route("/deleteuser", methods=["POST"])
def deleteuser():
    conn = None
    cursor = None

    try:
        user_id = request.form.get("user_id")

        conn = conn_db()
        cursor = conn.cursor()

        sql = "DELETE FROM account WHERE AccountID=%s"
        cursor.execute(sql, (user_id,))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("manageuser"))


#特定のMailAddressの場合の遷移判定/login.pyにいれたほうがいいかも

#@app.route('/')
#def index():


#    if MailAddress == 'hoge@hoge':
#       return redirect(url_for('managetop'))
#その他のuserはindex.htmlに遷移
#    else:
#        return render_template('index.html')

#@app.route('/managetop')
#def managetop():
#    return render_template('managetop.html')
#---------------------------------------------------

#manageuser
#dbの接続hetestからかえる(feature#4)