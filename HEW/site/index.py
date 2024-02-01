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

# /register
@app.route('/register')
def RegistrationPage():
    show_modal = False
    return render_template("registration.html",show_modal=show_modal)

# /register/
@app.route('/register/', methods=['POST'])
def Registration():
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
    
# /login
@app.route('/login')
def LoginPage():
    return render_template("login.html")

# /login/
@app.route('/login/', methods=['POST'])
def Login():
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
            PassMessage = "ログインできませんでした。ご確認の上もう一度お試しください。"
            return render_template("login.html", PassMessage=PassMessage)  

# /logout
@app.route('/logout')
def Logout():
    session['you'] = None
    return redirect(url_for('LoginPage'))

# /sell
@app.route('/sell')
def SellPage():
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    return render_template("sell.html")

# /sell_confirm
@app.route('/sell_confirm', methods=['POST'])
def SellConfirm():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        # ========== フォーム ==========
        # メイン画像
        sellimg_main = request.files.get('sellimg-main')
        
        # サブ画像(任意
        sellimgs_sub = request.files.getlist('sellimg-sub')
        if len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == '':
            print('フォーム:サブ画像は空です')
            
        # 商品名
        selltit = request.form['selltit']
        
        # 説明(任意
        if request.form['overview']:
            overview = request.form['overview']
        else:
            overview = None
            print('フォーム:商品悦明が未入力')
            
        # カテゴリー
        scategoryid = request.form['scategoryid']
        SCategory_Select = '''
        SELECT Name
        FROM Scategory
        WHERE SCategoryID = {0}
        '''.format(scategoryid)
        cursor.execute(SCategory_Select)
        SCategoryName = cursor.fetchone()[0]
            
        # サイズ
        postage = request.form['postage']
        Postage_Select = '''
        SELECT Size
        FROM Postage
        WHERE PostageID = {0}
        '''.format(postage)
        cursor.execute(Postage_Select)
        PostageSize = cursor.fetchone()[0]
        
        # 状態
        status = request.form['status']
        Status_Select = '''
        SELECT Name
        FROM Status
        WHERE StatusID = {0}
        '''.format(status)
        cursor.execute(Status_Select)
        StatusName = cursor.fetchone()[0]
        
        # 値段
        price = request.form['price']
        # ========== フォーム ==========
        

        # ========== 画像処理 ==========
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
            imgs = None
            print('機能:サブ画像が未入力の為ファイルを保存しません')
        # ========== 画像処理 ==========
            
        sell_data = [selltit,overview,SCategoryName,PostageSize,StatusName,price]
        form_data = [mainimg_path,imgs,selltit,overview,
                     scategoryid,postage,status,price]
        
        # 住所
        Address_Select = '''
        SELECT AddressID, Address, Post
        FROM Address
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(Address_Select)
        Address = cursor.fetchall()
        if Address == []:
            Address = None
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('sell_confirm.html',
                mainimg_path=mainimg_path, imgs=imgs, sell_data=sell_data, form_data=form_data, Address=Address)

# /sell/
@app.route('/sell/', methods=['POST'])
def Sell():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        # ========== フォーム ==========
        # メイン画像
        sellimg_main = request.form['sellimg-main']
        print("メイン：",sellimg_main)
        
        # サブ画像(任意
        if request.form.getlist('image_paths[]'):
            sellimgs_sub = request.form.getlist('image_paths[]')
            print("サブ：",sellimgs_sub)
        else:
            sellimgs_sub = None
            print('フォーム:サブ画像が未入力')
            
        # 商品名
        selltit = request.form['selltit']
        
        # 説明(任意
        if request.form['overview']:
            overview = request.form['overview']
        else:
            overview = None
            print('フォーム:商品悦明が未入力')
            
        # カテゴリー
        scategoryid = request.form['scategoryid']
            
        # サイズ
        postage = request.form['postage']
        
        # 状態
        status = request.form['status']
        
        # 値段
        price = request.form['price']
        
        # アクション
        sell_action = request.form['sell_action']
        # ========== フォーム ==========
            
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

        # サムネイルファイルのINSERT
        mainimg_sql = '''
        INSERT INTO 
        SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'1');
        '''.format(sellimg_main, sellid)
        cursor.execute(mainimg_sql)

        # サブファイルのINSERT(sellimgs_subの数分同じSellIDでINSERT)
        if sellimgs_sub:
            for subimg in sellimgs_sub:
               subimg_sql = '''
               INSERT INTO SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}', {1}, b'0');
               '''.format(subimg, sellid)
               cursor.execute(subimg_sql)
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('IndexPage'))

# trend
@app.route('/trend')
def TrendPage():
    return render_template("trend.html")

# /index
@app.route('/')
def IndexPage():
    
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    if you_list == None:
        return redirect(url_for('LoginPage'))
    
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
        
        if Account_Info == []:
            print('住所が未登録デス')
            return redirect(url_for('PersonalPage'))
        
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
        if Money == None:
            Money = int(0)
        
        Price_Select = '''
        SELECT Sell.Price, Postage.Price
        FROM Sell
        JOIN Postage ON Sell.PostageID = Postage.PostageID
        WHERE Sell.SellID = {0}
        '''.format(SellID)
        cursor.execute(Price_Select)
        # sell_price = cursor.fetchall()[0][0]
        prices = cursor.fetchall()[0]
        sell_pri = prices[0]
        postage_pri = prices[1]
        Price = int(sell_pri) + int(postage_pri)
        print(Price)
        
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
@app.route('/evaluate', methods=['POST'])
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
@app.route('/mypage')
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
    if proceed == None:
        proceed = int(0)
    
    # 所持金SELECT
    mone_sql = '''
    SELECT money 
    FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(mone_sql)
    money = cursor.fetchone()
    money = money[0]
    if money == None:
        money = int(0)
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(
        "mypage.html", proceed=proceed, money=money, 
        UserName=UserName, avg_evalate=avg_evalate
        )

# /favorite
@app.route('/favorite')
def FavoritePage():
    return render_template("favorite.html")

# /charge
@app.route('/charge', methods=['POST'])
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
        if money == None:
            money = int(0)
        
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
        
# /personal
@app.route('/personal')
def PersonalPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    name_error = request.args.get('error', None)
    pass_error = request.args.get('pass_error',None)
    mail_error = request.args.get('mail_error',None)
        
    # アカウントSELECT
    Account_Select = '''
    SELECT UserName, ProfIMG, Birthday, SexID, kanjiName, Furigana ,MailAddress
    FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Account_Select)
    AccountInfo = list(cursor.fetchone())
    for i in range(6):
        if AccountInfo[i] is None:
            AccountInfo[i] = '未登録'
    
    # アドレスSELECT
    Address_Select = '''
    SELECT Address, Post
    FROM Address
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Address_Select)
    AddressInfo = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('personal.html', AccountInfo=AccountInfo, AddressInfo=AddressInfo, 
                           MailAddress=MailAddress, name_error=name_error, pass_error=pass_error, mail_error=mail_error)

# /change_icon
@app.route('/change_icon', methods=['POST'])
def ChangeIcon():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        icon = request.files.get('icon')

        upload_path = "static/images/icon/"
        
        icon_path =  os.path.join(upload_path, icon.filename)
        icon.save(icon_path)
        
        ProfIMG_Update = '''
        UPDATE Account
        SET ProfIMG = '{0}'
        WHERE AccountID = {1};
        '''.format(icon_path,AccountID)
        cursor.execute(ProfIMG_Update)
    
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PersonalPage'))
    
# /change_username
@app.route('/change_username', methods=['POST'])
def ChangeUsername():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]

        username = request.form['username']
        
        # 登録済みユーザーネームSELECT
        UserName_Select = '''
        SELECT * FROM Account WHERE UserName='{0}';
        '''.format(username)
        cursor.execute(UserName_Select)
        existing_username = cursor.fetchone()
        
        if existing_username:
            name_error = '既に登録されたユーザー名です'
            return redirect(url_for('PersonalPage', name_error=name_error))
        else:
            Username_Update = '''
            UPDATE Account
            SET Username = '{0}'
            WHERE AccountID = {1};
            '''.format(username,AccountID)
            cursor.execute(Username_Update)
            
        
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('PersonalPage'))

# /change_mail
@app.route('/change_mail', methods=['POST'])
def ChangeMail():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        mailaddress = request.form['mailaddress']
        
        MailAddress_Select = '''
        SELECT * FROM Account WHERE MailAddress='{0}';
        '''.format(mailaddress)
        cursor.execute(MailAddress_Select)
        existing_mailaddress = cursor.fetchone()
        
        if existing_mailaddress:
            mail_error = '既に登録されたメールアドレスです'
            return redirect(url_for('PersonalPage', mail_error=mail_error))
        else:
            MailAddress_Update = '''
            UPDATE Account SET MailAddress = '{0}' 
            WHERE AccountID = {1};
            '''.format(mailaddress,AccountID)
            cursor.execute(MailAddress_Update)
                
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('PersonalPage'))

# /change_pass
@app.route('/change_pass', methods=['POST'])
def ChangePass():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        nowpass = request.form['nowpass']
        newpass = request.form['newpass']
        renewpass = request.form['renewpass']
        
        Password_Select ='''
        SELECT Password FROM Account
        WHERE AccountID = {0}
        '''.format(AccountID)
        cursor.execute(Password_Select)
        Password = cursor.fetchone()[0]
        
        
        if nowpass != Password:
            pass_error = '現在のパスワードが一致しません'
            return redirect(url_for('PersonalPage', pass_error=pass_error))
        
        elif newpass != renewpass:
            pass_error = '新しいパスワードが一致しません'
            return redirect(url_for('PersonalPage', pass_error=pass_error))
        
        else:
            Password_Update = '''
            UPDATE Account SET Password = '{0}'
            WHERE AccountID = {1};
            '''.format(newpass,AccountID)
            cursor.execute(Password_Update)
            pass_comp = 'パスワードが更新されました'
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('PersonalPage',pass_comp=pass_comp))
        
# /change_fullname
@app.route('/change_fullname', methods=['POST'])
def ChangeFullname():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        kanjiname = request.form['kanjiname']
        furigana = request.form['furigana']
        birthday = request.form['birthday']
        
        FullName_Update = '''
        UPDATE Account
        SET KanjiName = '{0}', Furigana = '{1}', birthday = '{2}'
        WHERE AccountID = {3}
        '''.format(kanjiname,furigana,birthday,AccountID)
        cursor.execute(FullName_Update)
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PersonalPage'))     
       
# /change_sex
@app.route('/change_sex', methods=['POST'])
def ChangeSex():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        sex = int(request.form['gender'])
        
        Sex_Update = '''
        UPDATE Account
        SET SexID = {0} WHERE AccountID = {1}
        '''.format(sex,AccountID)
        cursor.execute(Sex_Update)
        
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PersonalPage'))

# /add_address 
@app.route('/add_address', methods=['POST'])
def AddAddress():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        address = request.form['address']
        post = request.form['post']
        
        Address_Insert = '''
        INSERT INTO Address(Address, POST, AccountID)
        VALUE("{0}","{1}",{2})
        '''.format(address,post,AccountID)
        cursor.execute(Address_Insert)
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PersonalPage'))
    
# /del_address 
@app.route('/del_address', methods=['POST'])
def DelAddress():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
            
        address = request.form['address']
        post = request.form['post']
        
        Address_Delete = '''
        DELETE FROM Address
        WHERE Address = '{0}' AND POST = '{1}' AND AccountID = {2};
        '''.format(address,post,AccountID)
        cursor.execute(Address_Delete)
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('PersonalPage'))
    
# /draft_list
@app.route('/draft_list')
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
@app.route('/sell_list')
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
@app.route('/buy_list')
def BuyListPage():
    return render_template('buy_list.html')

# /insert
@app.route('/insert', methods=['GET', 'POST'])
def DB_Inset():
    conn = conn_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        TableName = request.form['TableName']
        btn_value = request.form['action']
        
        if TableName == 'Account':
            inputs = {
                # "TableID": request.form['TableID'],
                "UserName": request.form['UsNa'],
                "Password": request.form['Password'],
                "ProfIMG": request.form['ProfIMG'],
                "Birthday": request.form['Birthday'],
                "SexID": request.form['SexID'],
                "MailAddress": request.form['MaAd'],
                "KanjiName": request.form['KanjiName'],
                "Furigana": request.form['Furigana'],
                # "RegistDate": request.form['RegistDate'],
                "Money": request.form['Money']
            }
            
        elif TableName == 'Address':
            inputs = {
                # "TableID": request.form['TableID'],
                "Address": request.form['Address'],
                "POST": request.form['POST'],
                "AccountID": request.form['AcID']
            }
            
        elif TableName == 'Buy':
            inputs = {
                # "TableID": request.form['TableID'],
                "SellID": request.form['SellID'],
                "AccountID": request.form['AcID'],
                "Review": request.form['Review']
                # "Datetime": request.form['']
            }
            
        elif TableName == 'Chat':
            inputs = {
                # "TableID":request.form['TableID'],
                "AccountID":request.form['AcID'],
                "SellID":request.form['SellID'],
                "Content":request.form['Content']
                # "Datetime":request.form['Datetime']
            }
            
        else:
            return '予期しない TableName'
            
        # 辞書型のキー
        RowNames = ', '.join(inputs.keys())
        # 辞書型のデータ × length
        RowDatas = ', '.join(['%s'] * len(inputs))
            
        if btn_value == 'insert':
            Row_Insert = '''
            INSERT INTO {0} ({1}) VALUES ({2});
            '''.format(TableName,RowNames,RowDatas)
            #                          ↓ RowDatas 
            cursor.execute(Row_Insert, list(inputs.values()))
            print('実行:',Row_Insert)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('DB_' + TableName))
    else:
        return '予期しない request.method'
            
# /delete
@app.route('/delete', methods=['GET', 'POST'])
def DB_Delete():
    conn = conn_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        TableName = request.form['TableName']
        btn_value = request.form['action']
        
        if btn_value == 'delete':
            TableID = request.form['TableID']
            
            # 外部キー
            if TableName == 'Account':
                del_query = '''
                DELETE Account, Address, Numerical, Search, Nice, View, Chat, Sell, Buy
                FROM Account
                LEFT JOIN Address ON Account.AccountID = Address.AccountID
                LEFT JOIN Numerical ON Account.AccountID = Numerical.AccountID
                LEFT JOIN Search ON Account.AccountID = Search.AccountID
                LEFT JOIN Nice ON Account.AccountID = Nice.AccountID
                LEFT JOIN View ON Account.AccountID = View.AccountID
                LEFT JOIN Chat ON Account.AccountID = Chat.AccountID
                LEFT JOIN Sell ON Account.AccountID = Sell.AccountID
                LEFT JOIN Buy ON Account.AccountID = Buy.AccountID
                WHERE Account.AccountID = {0}
                '''.format(TableID)
                cursor.execute(del_query)
                print('実行:',del_query)
                conn.commit()

            # 主キー
            Row_Delete = '''
            DELETE FROM {0} WHERE {0}ID = {1};
            '''.format(TableName,TableID)
            cursor.execute(Row_Delete)
            print('実行:',Row_Delete)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('DB_' + TableName))

# /DB_Account
@app.route('/DB_Account', methods=['GET', 'POST'])
def DB_Account():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Account'
        cursor.execute("SELECT * FROM Account")
        Account = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Account.html', Account=Account,TableName=TableName)
        
# /DB_Sex
@app.route('/DB_Sex', methods=['GET', 'POST'])
def DB_Sex():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Sex'
        cursor.execute("SELECT * FROM Sex")
        Sex = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Sex.html', Sex=Sex,TableName=TableName)

# /DB_
@app.route('/DB_Address', methods=['GET', 'POST'])
def DB_Address():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Address'
        cursor.execute("SELECT * FROM Address")
        Address = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Address.html', Address=Address,TableName=TableName)

# /DB_
@app.route('/DB_Sell', methods=['GET', 'POST'])
def DB_Sell():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Sell'
        cursor.execute("SELECT * FROM Sell")
        Sell = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Sell.html', Sell=Sell,TableName=TableName)

# /DB_
@app.route('/DB_SellIMG', methods=['GET', 'POST'])
def DB_SellIMG():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'SellIMG'
        cursor.execute("SELECT * FROM SellIMG")
        SellIMG = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_SellIMG.html', SellIMG=SellIMG,TableName=TableName)

# /DB_
@app.route('/DB_Status', methods=['GET', 'POST'])
def DB_Status():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Status'
        cursor.execute("SELECT * FROM Status")
        Status = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Status.html', Status=Status,TableName=TableName)

# /DB_
@app.route('/DB_Mcategory', methods=['GET', 'POST'])
def DB_Mcategory():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Mcategory'
        cursor.execute("SELECT * FROM Mcategory")
        Mcategory = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Mcategory.html', Mcategory=Mcategory,TableName=TableName)

# /DB_
@app.route('/DB_Scategory', methods=['GET', 'POST'])
def DB_Scategory():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Scategory'
        cursor.execute("SELECT * FROM Scategory")
        Scategory = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Scategory.html', Scategory=Scategory,TableName=TableName)

# /DB_
@app.route('/DB_Tag', methods=['GET', 'POST'])
def DB_Tag():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Tag'
        cursor.execute("SELECT * FROM Tag")
        Tag = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Tag.html', Tag=Tag,TableName=TableName)

# /DB_
@app.route('/DB_Buy', methods=['GET', 'POST'])
def DB_Buy():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Buy'
        cursor.execute("SELECT * FROM Buy")
        Buy = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Buy.html', Buy=Buy,TableName=TableName)

# /DB_
@app.route('/DB_Nice', methods=['GET', 'POST'])
def DB_Nice():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Nice'
        cursor.execute("SELECT * FROM Nice")
        Nice = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Nice.html', Nice=Nice,TableName=TableName)

# /DB_
@app.route('/DB_View', methods=['GET', 'POST'])
def DB_View():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'View'
        cursor.execute("SELECT * FROM View")
        View = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_View.html', View=View,TableName=TableName)

# /DB_
@app.route('/DB_Chat', methods=['GET', 'POST'])
def DB_Chat():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Chat'
        cursor.execute("SELECT * FROM Chat")
        Chat = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Chat.html', Chat=Chat,TableName=TableName)

# /DB_
@app.route('/DB_Tax', methods=['GET', 'POST'])
def DB_Tax():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Tax'
        cursor.execute("SELECT * FROM Tax")
        Tax = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Tax.html', Tax=Tax,TableName=TableName)

# /DB_
@app.route('/DB_Postage', methods=['GET', 'POST'])
def DB_Postage():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Postage'
        cursor.execute("SELECT * FROM Postage")
        Postage = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Postage.html', Postage=Postage,TableName=TableName)

# /DB_
@app.route('/DB_Reply', methods=['GET', 'POST'])
def DB_Reply():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Reply'
        cursor.execute("SELECT * FROM Reply")
        Reply = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Reply.html', Reply=Reply,TableName=TableName)

# /DB_
@app.route('/DB_Layout', methods=['GET', 'POST'])
def DB_Layout():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Layout'
        cursor.execute("SELECT * FROM Layout")
        Layout = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Layout.html', Layout=Layout,TableName=TableName)

# /DB_
@app.route('/DB_Numerical', methods=['GET', 'POST'])
def DB_Numerical():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Numerical'
        cursor.execute("SELECT * FROM Numerical")
        Numerical = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Numerical.html', Numerical=Numerical,TableName=TableName)

# /DB_
@app.route('/DB_Search', methods=['GET', 'POST'])
def DB_Search():
        conn = conn_db()
        cursor = conn.cursor()
        TableName = 'Search'
        cursor.execute("SELECT * FROM Search")
        Search = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Search.html', Search=Search,TableName=TableName)

# 実行
if __name__ == ("__main__"):
    app.run(host="localhost", port=8000, debug=True)