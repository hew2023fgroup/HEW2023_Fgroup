#pychach
import sys
sys.dont_write_bytecode = True

from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector,os

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

# セッション鍵
app.secret_key="abcdefghijklmn"

# RenderTemplate------------------------------------------------------------
@app.route('/register')
def RegistrationPage():
    return render_template("registration.html")
@app.route('/login')
def LoginPage():
    return render_template("login.html")
@app.route('/index')
def IndexPage():
    return render_template("index.html")
@app.route('/sell')
def SellPage():
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
        print(UserName, "でログイン中...")
    return render_template("sell.html")
@app.route('/mypage')
def MyPage():
    return render_template("mypage.html")
@app.route('/favorite')
def FavoritePage():
    return render_template("favorite.html")
@app.route('/trend')
def TrendPage():
    return render_template("trend.html")
# ------------------------------------------------------------

# /register/
@app.route('/register/',methods=['POST'])   #小濱俊史
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
        sql = '''
               INSERT INTO Account 
               (UserName, Password, MailAddress) VALUES ('{0}', '{1}', '{2}');
              '''.format(username, password, email)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        
        return render_template("login.html")
   
# /login/
@app.route('/login/', methods=['POST']) #小濱俊史
def login():
    if request.method == 'POST':
        
        # フォーム
        email = request.form['email']
        password = request.form['password']
        
        # SELECT
        conn = conn_db()
        cursor = conn.cursor()
        sql = '''
               SELECT MailAddress, Password 
               FROM Account WHERE MailAddress = '{0}' AND Password = '{1}';
              '''.format(email, password)
        cursor.execute(sql)
        
        # 認証
        user = cursor.fetchone()
        if user:
            # 成功
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

# /sell/
@app.route('/sell/', methods=['POST'])  #小濱俊史
def Sell():    
    if request.method == 'POST':
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        # フォーム
        sellimgs = request.files.getlist('sellimg')
        selltit = request.form['selltit']
        overview = request.form['overview']
        scategoryid = request.form['scategoryid']
        postage = request.form['postage']
        status = request.form['status']
        price = request.form['price']
        
        # 入力確認
        print("AccountID:", AccountID)
        print("selltit:", selltit)
        print("overview:", overview)
        print("scategory:", scategoryid)
        print("postage:", postage)
        print("status:", status)
        print("price:", price)
        
        # ファイルを保存(送信した画像数分imgsへ挿入)
        upload_path = "static/images/sell/"
        imgs = []
        for sellimg in sellimgs:
            sellimg.save(os.path.join(upload_path, sellimg.filename))
            imgs.append(os.path.join(upload_path, sellimg.filename))
        print(imgs)
        
        conn = conn_db()
        cursor = conn.cursor()
        
        # SellのINSERT
        sell = '''
                INSERT INTO Sell 
                (Name, Price, PostageID, StatusID, Overview, SCategoryID, AccountID) 
                VALUES ('{0}',{1},{2},{3},'{4}',{5},{6});
               '''.format(selltit,price,postage,status,overview,scategoryid,AccountID)
        cursor.execute(sell)
        sellid = cursor.lastrowid
        print("SellID",sellid)
        
        # IMGのINSERT(imgsの数分同じSellIDでINSERT)
        for img in imgs:
            img = '''
                   INSERT INTO SellIMG (SellIMG, SellID) VALUES ('{0}',{1});
                  '''.format(img, sellid)
            cursor.execute(img)
        
        conn.commit()
        cursor.close()
        
        return render_template('sell.html')