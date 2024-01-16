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

# /register
@app.route('/register')
def RegistrationPage():
    show_modal = False
    return render_template("registration.html",show_modal=show_modal)

# /input
@app.route('/input', methods=['POST'])
def InputRegister():
    show_modal = True
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        input_data = [username, email, password]
        
        # 登録済みメールアドレスSELECT
        sql = "SELECT * FROM Account WHERE MailAddress='{0}'".format(email)
        cursor.execute(sql)
        existing_mail = cursor.fetchone()
        
        # 登録済みユーザーネームSELECT
        UserName_Select = "SELECT * FROM Account WHERE UserName='{0}'".format(username)
        cursor.execute(UserName_Select)
        existing_username = cursor.fetchone()
        
        if existing_username and existing_mail:
            check_name = False
            check_mail = False
            check_pass = True
            error = "既に登録されています"
        elif existing_username:
            check_name = False
            check_mail = True
            check_pass = True
            error = "既に登録されたユーザー名です"
        elif existing_mail:
            check_name = True
            check_mail = False
            check_pass = True
            error = "既に登録されたアドレスです"
        else:
            error = None
            check_name = True
            check_mail = True
            check_pass = True
        
        checks = [check_name, check_mail, check_pass]
            
    
        return render_template('registration.html',show_modal=show_modal, input_data=input_data, error=error, checks=checks)

# /register/
@app.route('/register/',methods=['POST'])   #小濱俊史
def register():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
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
        
        # 任意
        sellimgs_sub = request.files.getlist('sellimg-sub')
        if len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == '':
            print('フォーム:サブ画像は空です')
            
        selltit = request.form['selltit']
        
        # 任意
        if request.form['overview']:
            overview = request.form['overview']
        else:
            overview = None
            print('フォーム:商品悦明が未入力')
            
        scategoryid = request.form['scategoryid']
        postage = request.form['postage']
        status = request.form['status']
        price = request.form['price']
        
        sell_action = request.form['sell_action']

        # 保存先パス
        upload_path = "static/images/sell/"
        
        # サムネイルファイル保存
        mainimg_path =  os.path.join(upload_path, sellimg_main.filename)
        sellimg_main.save(mainimg_path)
        
        # サブファイル保存(送信した画像数分imgsへ挿入)
        if not (len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == ''):
            imgs = []
            for sellimg in sellimgs_sub:
                img_path = os.path.join(upload_path, sellimg.filename)
                sellimg.save(img_path)
                imgs.append(img_path)
        else:
            print('機能:サブ画像が未入力の為ファイルを保存しません')
            
        # SellのINSERT
        sell_sql = '''
        INSERT INTO Sell 
        (Name, Price, PostageID, StatusID, Overview, SCategoryID, AccountID) 
        VALUES ('{0}',{1},{2},{3},'{4}',{5},{6});
        '''.format(selltit,price,postage,status,overview,scategoryid,AccountID)
        cursor.execute(sell_sql)
        sellid = cursor.lastrowid
        
        # 下書き
        if sell_action == 'draft':
            
            Draft_Update = '''
            UPDATE Sell
            SET Draft = 0
            WHERE SellID = {0};
            '''.format(sellid)
            cursor.execute(Draft_Update)
            
        print('''
              「出品完了」
              SellID:{0}
              Name:{1}
              サムネイル:{2}
              '''.format(sellid,selltit,mainimg_path))
        
        # サムネイルファイルのINSERT
        mainimg_sql = '''
        INSERT INTO 
        SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'1');
        '''.format(mainimg_path, sellid)
        cursor.execute(mainimg_sql)
        
        # サブファイルのINSERT(imgsの数分同じSellIDでINSERT)
        if not (len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == ''):
            for subimg in imgs:
                subimg_sql = '''
                INSERT INTO 
                SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'0');
                '''.format(subimg, sellid)
                cursor.execute(subimg_sql)
        else:
            print('機能:サブ画像が未入力の為INSERTしません')
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('sell.html')

# /index
@app.route('/index')
def IndexPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # 出品取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きではない。
    sql = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL AND SellIMG.ThumbnailFlg = 0x01 AND Sell.Draft = 0x01;
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
    error = request.args.get('error', None)
    conn = conn_db()
    cursor = conn.cursor()
    
    # 商品情報のSELECT
    info = '''
    SELECT SellIMG.SellIMG, Sell.Name, Sell.Price, Scategory.Name, Status.Name, Sell.Overview
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    JOIN Scategory ON Sell.SCategoryID = Scategory.ScategoryID
    JOIN Status ON Sell.StatusID = Status.StatusID
    WHERE Sell.SellID = {0};
    '''.format(sellid)
    cursor.execute(info)
    products = cursor.fetchall()
    
    # 関数割り当て
    imgs = [img[0] for img in products] 
    name = products[0][1]
    price = products[0][2]
    scategory = products[0][3]
    status = products[0][4]
    overview = products[0][5]
    
    # 出品者のAccountIDのSELECT
    acc = '''
    SELECT Sell.AccountID, Account.UserName 
    FROM Sell 
    JOIN Account ON Sell.AccountID = Account.AccountID
    WHERE SellID = {0};
    '''.format(sellid)
    cursor.execute(acc)
    sell_acc = cursor.fetchone()
    
    # 平均評価値のSELECTx2
    evalscore_sql = '''
    SELECT AVG(Review) 
    FROM Buy 
    WHERE SellID IN (SELECT SellID FROM Sell WHERE AccountID = {0});
    '''.format(sell_acc[0])
    cursor.execute(evalscore_sql)
    avg_evalate = cursor.fetchone()[0]
    if avg_evalate is None:
        avg_evalate = 0
    
    print('''
          {0}さんの
          評価値の平均は({1})です。
          '''.format(sell_acc[1], avg_evalate))
    
    # 出品取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きではない。
    sells = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL AND SellIMG.ThumbnailFlg = 0x01 AND Sell.Draft = 0x01;
    '''
    cursor.execute(sells)
    sells = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(
        "product.html",imgs=imgs, name=name, overview=overview,
        price=price, sellid=sellid, scategory=scategory, 
        status=status, avg_evalate=avg_evalate, sell_acc=sell_acc, sells=sells, 
        error=error
        )
    
# /buy
@app.route('/buy', methods=['POST'])
def Buy():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        SellID = request.form['SellID']
        
        # 出品情報のSELECT
        Sell_Select = '''
        SELECT SellIMG.SellIMG, Sell.Name, Sell.Overview, Sell.Price, Postage.Price
        FROM Sell
        JOIN SellIMG ON Sell.SellID = SellIMG.SellID
        JOIN Postage ON Sell.PostageID = Postage.PostageID
        WHERE Sell.SellID = {0} AND SellIMG.ThumbnailFlg = 0x01;
        '''.format(SellID)
        cursor.execute(Sell_Select)
        Sell_Info = cursor.fetchall()
        
        Total_Price = int(Sell_Info[0][3]) + int(Sell_Info[0][4])
        
        # ユーザー情報SELECT
        Account_Select = '''
        SELECT Address, Post
        FROM Address
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(Account_Select)
        Account_Info = cursor.fetchall()
        
        # 配達時間計算
        CurrentTime = datetime.now()
        FutureTime24 = CurrentTime + timedelta(hours=24)
        FutureTime48 = CurrentTime + timedelta(hours=48)

        After24H = FutureTime24.strftime('%Y年%m月%d日')
        After48H = FutureTime48.strftime('%Y年%m月%d日')

        return render_template(
            'pay_comp.html', Sell_Info=Sell_Info[0], Account_Info=Account_Info[0], 
            UserName=UserName, Total_Price=Total_Price, SellID=SellID, After48H=After48H,
            After24H=After24H,
            )

# /pay
@app.route('/pay', methods=['POST'])
def PayPage():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        SellID = request.form['SellID']
        
        # 所持金SELECT
        Money_Select = '''
        SELECT Money
        FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(Money_Select)
        Money = cursor.fetchall()[0][0]
        
        Price_Select = '''
        SELECT Price
        FROM Sell
        WHERE SellID = {0};
        '''.format(SellID)
        cursor.execute(Price_Select)
        Price = cursor.fetchall()[0][0]
        
        # 所持金が足りているか
        Balance = int(Money) - int(Price)
        if Balance >= 0:
            
            # 所持金UPDATE
            Money_Update = '''
            UPDATE Account
            SET Money = {0}
            WHERE AccountID = {1};
            '''.format(Balance,AccountID)
            cursor.execute(Money_Update)
            
            # 購入INSERT
            Buy_Insert = '''
            INSERT INTO Buy (SellID, AccountID) VALUES ({0},{1});
            '''.format(SellID, AccountID)
            cursor.execute(Buy_Insert)
            BuyID = cursor.lastrowid
            
            print('''
                「購入されました」
                購入者ID:{0}
                出品ID:{1} ... {2}円
                購入ID:{3}
                所持金:{4}円 -> {5}円
                '''.format(AccountID,SellID,Price,BuyID,Money,Balance))
            
            # 出品者SELECT
            Seller_Select = '''
            SELECT AccountID
            FROM Sell
            WHERE SellID = {0};
            '''.format(SellID)
            cursor.execute(Seller_Select)
            SellerID = cursor.fetchall()[0][0]
            
            # 出品者の残高SELECT
            Money_Select = '''
            SELECT Money
            FROM Account
            WHERE AccountID = {0};
            '''.format(SellerID)
            cursor.execute(Money_Select)
            SellerMoney = cursor.fetchall()[0][0]
            
            Proceed = int(SellerMoney) + int(Price)
            
            # 売り上げUPDATE
            Proceed_Update = '''
            UPDATE Account 
            SET Money = {0}
            WHERE AccountID = {1};
            '''.format(Proceed,SellerID)
            cursor.execute(Proceed_Update)
        
            print('''
                  「入金されました」
                  出品者残高:{0}円 -> {1}円
                  '''.format(SellerMoney,Proceed))
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('BuyCompPage', BuyID=BuyID))
        
        # 所持金が足りない
        else:
            error = True
            return redirect(url_for('ProductPage',sellid=SellID, error=error))

# /buycomp/<BuyID>
@app.route('/buycomp/<BuyID>')
def BuyCompPage(BuyID):

    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
        
    return render_template("buy_comp.html", MailAddress=MailAddress, BuyID=BuyID)
    
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
    if avg_evalate is None:
        avg_evalate = 0
    
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
    return render_template(
        "mypage.html", proceed=proceed, money=money, 
        UserName=UserName, avg_evalate=avg_evalate
        )

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
    
# /draft_list
@app.route('/draft_list')   # 小濱俊史
def DraftPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    # 下書き取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きである、商品を出したのが自分。
    Draft_Select = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL AND SellIMG.ThumbnailFlg = 0x01 AND Sell.Draft = 0x00 AND Sell.AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Draft_Select)
    Drafts = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('draft_list.html',Drafts=Drafts)

# /sell_list
@app.route('/sell_list')   # 小濱俊史
def SellListPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    # 下書き取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きでない、商品を出したのが自分。
    Sell_Select = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL AND SellIMG.ThumbnailFlg = 0x01 AND Sell.Draft = 0x01 AND Sell.AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Sell_Select)
    Sells = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('sell_list.html',Sells=Sells)

# /buy_list
@app.route('/buy_list')   # 小濱俊史
def BuyListPage():
    return render_template('buy_list.html')


# 実行
if __name__ == ("__main__"):
    app.run(host="localhost", port=8000, debug=True)