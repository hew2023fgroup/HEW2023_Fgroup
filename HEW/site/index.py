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
        conn = conn_db()
        cursor = conn.cursor()
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 登録済みメールアドレスSELECT
        sql = "SELECT * FROM Account WHERE MailAddress='{0}'".format(email)
        cursor.execute(sql)
        existing_user = cursor.fetchone()

        if existing_user:
            MailMessage = "！！既に登録されたアドレスです！！"
            return render_template("registration.html", MailMessage=MailMessage)

        # メールアドレス未登録のINSERT
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
        conn = conn_db()
        cursor = conn.cursor()
        
        email = request.form['email']
        password = request.form['password']
        
        # パスワード認証のSELECT
        sql = '''
        SELECT MailAddress, Password 
        FROM Account WHERE MailAddress = '{0}' AND Password = '{1}';
        '''.format(email, password)
        cursor.execute(sql)
        user = cursor.fetchone()
        
        # 認証
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
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        sellimg_main = request.files.get('sellimg-main')
        sellimgs_sub = request.files.getlist('sellimg-sub')
        selltit = request.form['selltit']
        overview = request.form['overview']
        scategoryid = request.form['scategoryid']
        postage = request.form['postage']
        status = request.form['status']
        price = request.form['price']
        
        # 保存先パス
        upload_path = "static/images/sell/"
        
        # サムネイルファイル保存
        mainimg_path =  os.path.join(upload_path, sellimg_main.filename)
        sellimg_main.save(mainimg_path)
        
        # サブファイル保存(送信した画像数分imgsへ挿入)
        imgs = []
        for sellimg in sellimgs_sub:
            img_path = os.path.join(upload_path, sellimg.filename)
            sellimg.save(img_path)
            imgs.append(img_path)
            
        # SellのINSERT
        sell_sql = '''
        INSERT INTO Sell 
        (Name, Price, PostageID, StatusID, Overview, SCategoryID, AccountID) 
        VALUES ('{0}',{1},{2},{3},'{4}',{5},{6});
        '''.format(selltit,price,postage,status,overview,scategoryid,AccountID)
        cursor.execute(sell_sql)
        sellid = cursor.lastrowid
        
        print('''
              「出品完了」
              SellID:{0}
              Name:{1}
              サムネイル:{2}
              サブ:{3}
              '''.format(sellid,selltit,mainimg_path,imgs))
        
        # サムネイルファイルのINSERT
        mainimg_sql = '''
        INSERT INTO SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'1');
        '''.format(mainimg_path, sellid)
        cursor.execute(mainimg_sql)
        
        # サブファイルのINSERT(imgsの数分同じSellIDでINSERT)
        for subimg in imgs:
            subimg_sql = '''
            INSERT INTO SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'0');
            '''.format(subimg, sellid)
            cursor.execute(subimg_sql)
            
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
    
    # 出品取得のSELECT
    sql = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL AND SellIMG.ThumbnailFlg = 0x01;
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
    
    # 商品情報のSELECT
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
    return render_template("product.html", sellid=sellid, product=product, error=request.args.get('error'))
# --------------------------- 削除予定 ---------------------------------
    

# /buy/
@app.route('/buy/', methods=['POST'])  #小濱俊史
def Buy():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
                
        sellid = request.form['sellid']
        
        # 所持金SELECT
        wal_sql = '''
        SELECT Money FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(wal_sql)
        wallet = cursor.fetchone()[0]
        
        # 金額SELECT
        pri_sql = '''
        SELECT Price FROM Sell 
        WHERE SellID = {0};
        '''.format(sellid)
        cursor.execute(pri_sql)
        price = cursor.fetchone()[0]
        
        # 所持金が足りているか
        balance = int(wallet) - int(price)
        if balance >= 0:
            
            # 所持金UPDATE
            paid_sql = '''
            UPDATE Account 
            SET Money = {0}
            WHERE AccountID = {1};
            '''.format(balance,AccountID)
            cursor.execute(paid_sql)
            
            # 購入INSERT
            buy_sql = '''
                INSERT INTO Buy (SellID, AccountID) VALUES ({0},{1});
                '''.format(sellid, AccountID)
            cursor.execute(buy_sql)
            buyid = cursor.lastrowid
            print('''
                「購入されました」
                購入者AccountID:{0}
                SellID:{1} ... {2}円
                BuyID:{3}
                Wallet:{4}円 -> {5}円
                '''.format(AccountID,sellid,price,buyid,wallet,balance))
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('PayPage',buyid=buyid))
        else:    
            error = '所持金が足りません'
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('ProductPage',sellid=sellid,error=error))

# /evaluate
@app.route('/evaluate', methods=['POST']) # 小濱俊史
def Evaluate():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        buyid = request.form['buyid']
        eval = request.form['rate']
        
        # 評価値のUPDATE
        eval_sql = '''
        UPDATE Buy 
        SET Review = {0}
        WHERE BuyID = {1};
        '''.format(eval, buyid)
        cursor.execute(eval_sql)
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('IndexPage'))

# /pay
@app.route('/pay/<int:buyid>')  # 小濱俊史
def PayPage(buyid):
    conn = conn_db()
    cursor = conn.cursor()
    
    # 決済情報SELECT
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
    
    # 購入日時SELECT
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
    
    # 評価値のSELECT
    evalget_sql = '''
    SELECT Review FROM Buy
    WHERE BuyID = {0};
    '''.format(buyid)
    cursor.execute(evalget_sql)
    eval = cursor.fetchone()[0]
    
    if eval is None:
        eval = 0
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("pay_comp.html", buy=buy, delidate=delidate, buyid=buyid, eval=eval)
    
# /mypage
@app.route('/mypage')   # 小濱俊史
def MyPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    # 平均評価値のSELECTx2
    evalscore_sql = '''
    SELECT AVG(Review) 
    FROM Buy 
    WHERE SellID IN (SELECT SellID FROM Sell WHERE AccountID = {0});
    '''.format(AccountID)
    cursor.execute(evalscore_sql)
    avg_evalate = cursor.fetchone()[0]
    
    print('''
          評価値の平均は({0})です。
          '''.format(avg_evalate))
    
    # 売り上げSELECT
    proc_sql = '''
    SELECT SUM(Sell.Price)
    FROM Sell
    JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Sell.AccountID = {0};
    '''.format(AccountID)
    cursor.execute(proc_sql)
    proceed = cursor.fetchone()[0]
    
    # 所持金SELECT
    mone_sql = '''
    SELECT money 
    FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(mone_sql)
    money = cursor.fetchone()
    money = money[0]
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("mypage.html", proceed=proceed, money=money, UserName=UserName, avg_evalate=avg_evalate)

# /charge
@app.route('/charge', methods=['POST'])   # 小濱俊史
def ChargePage():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        charge = request.form['charge']
            
        # 所持金SELECT
        out_sql = '''
        SELECT money 
        FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(out_sql)
        money = cursor.fetchone()
        money = money[0]
        
        charged = int(money) + int(charge)
        
        # 所持金UPDATE
        in_sql = '''
        UPDATE Account
        SET money = {0}
        WHERE AccountID = {1};
        '''.format(charged,AccountID)
        cursor.execute(in_sql)
        
        print('''
              「チャージされました」
              前：{0}
              後：{1}
              '''.format(money,charged))
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return  redirect(url_for('MyPage'))

# 実行
if __name__ == ("__main__"):
    app.run(host="localhost", port=8000, debug=True)