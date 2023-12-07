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

#---------------------------------------------------
#各ページへの遷移(manageページにある分だけ)
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

@app.route('/favorite')
def FavoritePage():
    return render_template("favorite.html")

@app.route('/mylist')
def MylistPage():
    return render_template("mylist.html")

@app.route('/mypage')
def MyPage():
    return render_template("mypage.html")

@app.route('/personal')
def PersonalPage():
    return render_template("personal.html")

@app.route('/product')
def ProductPage():
    return render_template("product.html")

@app.route('/sell')
def SellPage():
    return render_template("sell.html")

@app.route('/viewlog')
def ViewlogPage():
    return render_template("viewlog.html")

#-------------------------------------------------------

# ユーザー情報を表示
# Accountデータとそれに付随する情報をすべて一覧表示(住所や性別も外部キーのままでなくvalueを表示)
@app.route("/manageuser")
def ManageuserPage():
    #DB接続オブジェクトの取得
    conn = conn_db()
    
    try:
        # sql実行処理のコピー
        cursor = conn.cursor()
        
        # AccountとSexとAddressを内部結合して実行
        sql = '''select ac.AccountID,ac.UserName,ac.Password,ac.ProfIMG,ac.Birthday,
            s.Sex,ac.MailAddress,ac.KanjiName,ac.Furigana,ac.RegistDate,ac.Money,ad.Address,ad.POST
            from Account as ac, Sex as s, Address as ad
            WHERE ac.SexID = s.SexID and ac.AccountID = ad.AccountID;'''
        cursor.execute(sql)
        
        # recordsに格納(exp:全データ数が3行なら3タプルがrecordsリストに格納されている状態)
        records = cursor.fetchall()
        return render_template("manageuser.html", result=records)
        
        
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    

# @app.route("/manageuser")
# def ManageuserPage():
#     conn = conn_db()
#     cursor = conn.cursor()
#     try:
#         sql = "SELECT * FROM account"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         return render_template("manageuser.html", result=result)
#     except mysql.connector.Error as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

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

    return redirect(url_for("ManageuserPage"))

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

        sql = "UPDATE account SET MailAddress=%s WHERE AccountID=%s"
        cursor.execute(sql, (new_email, user_id))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("ManageuserPage"))

# ユーザーを削除
@app.route("/deleteuser", methods=["POST"])
def deleteuser():
    conn = None
    cursor = None

    try:
        user_id = request.form.get("user_id")

        conn = conn_db()
        cursor = conn.cursor()
#岡郁也
        sql = "delete ad from Address as ad JOIN Account as ac ON ad.AccountID = ac.AccountID WHERE ac.AccountID = %s;"
        cursor.execute(sql, (user_id,))
        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for("ManageuserPage"))


#特定のMailAddressの場合の遷移判定/login.pyにいれたほうがいいかも

#@app.route('/')
#def index():


#    if MailAddress == 'hoge@hoge':
#       return redirect(url_for('ManagetopPage'))
#その他のuserはindex.htmlに遷移
#    else:
#        return render_template('index.html')
