from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector,os
from datetime import datetime, timedelta

# カレントディレクトリをスクリプトディレクトリに固定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
@app.route('/')
def LoginPage():
    return render_template("login.html")

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
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
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
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('IndexPage'))
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
            img_path = os.path.join(upload_path, sellimg.filename)
            sellimg.save(img_path)
            imgs.append(img_path)
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
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('sell.html')



# 仮の商品(簡易/詳細)ページ ----------------------------------------------------------
# /index
@app.route('/index')
def IndexPage():
    
    conn = conn_db()
    cursor = conn.cursor()
    
    sql = '''
        SELECT Sell.SellID, Sell.Name, Sell.Price, MIN(SellIMG.SellIMG)
        FROM Sell
        JOIN SellIMG ON Sell.SellID = SellIMG.SellID
        LEFT JOIN Buy ON Sell.SellID = Buy.SellID
        WHERE Buy.SellID IS NULL
        GROUP BY Sell.SellID
        '''
    cursor.execute(sql)
    sells = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("index.html", sells=sells)

# /product/<sellid>
@app.route('/product/<sellid>')
def ProductPage(sellid):
    
    conn = conn_db()
    cursor = conn.cursor()
    
    sql = '''
        SELECT Name, Price FROM Sell WHERE SellID = '{0}';
        '''.format(sellid)
    cursor.execute(sql)
    product = cursor.fetchone()
    print("アクセス中の商品 ->",product[0])
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("product.html", sellid=sellid, product=product)
# --------------------------- 削除予定 ---------------------------------
    

# /buy/
@app.route('/buy/', methods=['POST'])  #小濱俊史
def Buy():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        sellid = request.form['sellid']
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
                
        sql = '''
            INSERT INTO Buy (SellID, AccountID) VALUES ({0},{1});
            '''.format(sellid, AccountID)
        cursor.execute(sql)
        buyid = cursor.lastrowid
        print('''
              「購入されました」
              購入者AccountID:{0}
              SellID:{1}
              BuyID:{2}
              '''.format(sellid,AccountID,buyid))
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PayPage',buyid=buyid))

# /pay
@app.route('/pay/<int:buyid>')  # 小濱俊史
def PayPage(buyid):
    conn = conn_db()
    cursor = conn.cursor()
    
    pay_sql = '''
        SELECT Buy.BuyID, Buy.DateTime, Sell.Name, Sell.Price, Account.UserName, Postage.Price
        FROM Buy
        INNER JOIN Sell ON Buy.SellID = Sell.SellID
        INNER JOIN Account ON Sell.AccountID = Account.AccountID
        INNER JOIN Postage ON Sell.PostageID = Postage.PostageID
        WHERE Buy.BuyID = {0};
        '''.format(buyid)
    cursor.execute(pay_sql)
    buy = cursor.fetchone()
    
    del_sql = '''
        SELECT Buy.DateTime
        FROM Buy
        WHERE Buy.BuyID = {0};
        '''.format(buyid)
    cursor.execute(del_sql)
    buydate = cursor.fetchone()
    
    # 配達日時指定プログラム
    if buydate:
        # リストから変換
        buydate = buydate[0]
        # 文字列へ変換
        buydate = datetime.strptime(str(buydate), '%Y-%m-%d %H:%M:%S')
        # +48時間(配達したい日時へ設定)
        delidate = buydate + timedelta(hours=48)
        # 形式変更
        delidate = delidate.strftime('%Y/%m/%d頃 予定')
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("pay_comp.html", buy=buy, delidate=delidate)
    else:
        return render_template("pay_comp.html", buy=buy, delidate='NULL')
    
# 実行
if __name__ == ("__main__"):
    app.run(host="localhost", port=8000, debug=True)