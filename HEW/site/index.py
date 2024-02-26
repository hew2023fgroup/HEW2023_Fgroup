from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import mysql.connector,os,random,ast
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
    
# #########################################
# ログイン
# #########################################

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
        id = cursor.lastrowid
        
        Layout_Insert = '''
        INSERT INTO Numerical(Numerical, LayoutID, AccountID)
        VALUES('#F00', 1, {0}), ('#FFF', 2, {0}), ('#FFF', 3, {0}), ('#F00', 4, {0}), ('#000', 5, {0}), ('#000', 6, {0}), ('#FFF', 7, {0}), 
        ('static/images/slide/slide01.jpg', 4, {0}), ('static/images/slide/slide05.jpg', 5, {0}), 
        ('static/images/slide/slide08.jpg', 6, {0}), ('static/images/slide/slide10.jpg', 7, {0});
        '''.format(id)
        cursor.execute(Layout_Insert)
        
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
            
            # セッションへレイアウト情報を保存
            Layout_Select = '''
            SELECT LayoutID, Numerical
            FROM Numerical
            WHERE AccountID = {0};
            '''.format(you[0][0])
            cursor.execute(Layout_Select)
            print('実行:',Layout_Select)
            layout_value = cursor.fetchall()
            session['layout'] = layout_value

            Simple_Select = '''
            SELECT SlideShowFlg, SimpleThumbFlg, SimplePriceFlg
            FROM Account
            WHERE AccountID = {0};
            '''.format(you[0][0])
            cursor.execute(Simple_Select)
            print('実行:',Simple_Select)
            simple_value = list(cursor.fetchone())
            session['simple'] = simple_value
            
            Slide_Select = '''
            SELECT Numerical, NumericalID 
            FROM Numerical
            WHERE AccountID = {0} 
            AND LayoutID IN (8, 9, 10, 11);
            '''.format(you[0][0])
            cursor.execute(Slide_Select)
            print('実行:',Slide_Select)
            slide_value = cursor.fetchall()
            print('slide_session:',slide_value)
            session['slideimg'] = slide_value
            
            # CLOSE
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('IndexPage'))
        else:
            # 失敗
            PassMessage = "ログインできませんでした。ご確認の上もう一度お試しください。"
            return render_template("login.html", PassMessage=PassMessage)  

# #########################################
# 出品購入
# #########################################

# /sell
@app.route('/sell')
def SellPage():
    conn = conn_db()
    cursor = conn.cursor()
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *:not(input){{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
            .btn05{{
                background-color: {3} !important
            }}
        </style>
    '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
        
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("sell.html",icon=icon, UserName=UserName,
                           style=style, layout_value=layout_value)

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
    
        layout_value = session.get('layout')
        print('layout:',layout_value)

        style = '''
            <style>
                *:not(input){{
                    color: {4} !important;
                }}
                html {{
                    background-color: {2} !important;
                }}
                .left-nav p {{
                    color: #000 !important;
                }}
                .right-nav ul li a, .right-nav ul li p{{
                    color: #000 !important;
                }}
                #btn{{
                    background-color: {0} !important;
                    color: {1} !important;
                }}
                footer {{
                    background-color: {5} !important;
                }}
                footer p{{
                    color: {6} !important;
                }}
                .btn05{{
                    background-color: {3} !important
                }}
            </style>
            '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])

        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
        # ========== フォーム ==========
        # メイン画像
        # sellimg_main = request.files.get('sellimg-main')
        
        # サブ画像(任意
        # sellimgs_sub = request.files.getlist('sellimg-sub')
        # if len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == '':
        #     print('フォーム:サブ画像は空です')
            
            
        # 新画像
        input_imgs = request.files.getlist('uploadInput')
        select = request.form['select']
        print('new:',input_imgs)
        print('select',select)
            
            
        # 商品名
        selltit = request.form['selltit']
        
        # 説明(任意
        if request.form['overview']:
            overview = request.form['overview']
        else:
            overview = None
            print('フォーム:商品悦明が未入力')
            
        # タグ
        if 'tag0' in request.form and request.form['tag0']:
            tags = []
            for i in range(20):
                key = 'tag' + str(i)
                if key in request.form:
                    tags.append(request.form[key])
        else:
            tags = None
            
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
        # mainimg_path =  os.path.join(upload_path, sellimg_main.filename)
        # sellimg_main.save(mainimg_path)

        # サブファイル保存(送信した画像数分imgsへ挿入)
        # if not (len(sellimgs_sub) == 1 and sellimgs_sub[0].filename == ''):
        #     imgs = []
        #     for sellimg in sellimgs_sub:
        #         img_path = os.path.join(upload_path, sellimg.filename)
        #         sellimg.save(img_path)
        #         imgs.append(img_path)
        # else:
        #     imgs = None
        #     print('機能:サブ画像が未入力の為ファイルを保存しません')
        
        #new
        if not (len(input_imgs) == 1 and input_imgs[0].filename == ''):
            imgs = []
            for sellimg in input_imgs:
                img_path = os.path.join(upload_path, sellimg.filename)
                sellimg.save(img_path)
                imgs.append(img_path)
        else:
            imgs = None 
        # ========== 画像処理 ==========
            
        sell_data = [selltit,overview,SCategoryName,PostageSize,StatusName,price]
        # form_data = [mainimg_path,imgs,selltit,overview,scategoryid,postage,status,price]
        form_data = [imgs,selltit,overview,scategoryid,postage,status,price]
        
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
        # return render_template('sell_confirm.html', icon=icon, UserName=UserName,
        #         mainimg_path=mainimg_path, imgs=imgs, sell_data=sell_data, form_data=form_data, Address=Address, tags=tags)
        return render_template('sell_confirm.html', icon=icon, UserName=UserName,select=select,
                imgs=imgs, sell_data=sell_data, form_data=form_data, Address=Address, tags=tags,
                style=style, layout_value=layout_value)

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
        # sellimg_main = request.form['sellimg-main']
        # print("メイン：",sellimg_main)
        
        # サブ画像(任意
        # if request.form.getlist('image_paths[]'):
        #     sellimgs_sub = request.form.getlist('image_paths[]')
        #     print("サブ：",sellimgs_sub)
        # else:
        #     sellimgs_sub = None
        #     print('フォーム:サブ画像が未入力')
            
        images = request.form['images']
        images = ast.literal_eval(images)
        print('images:',images)
        select = request.form['select']
        select = 'static/images/sell/' + select
        print('select:',select)
        
        # 商品名
        selltit = request.form['selltit']
        
        # 説明(任意
        if request.form['overview']:
            overview = request.form['overview']
        else:
            overview = None
            print('フォーム:商品悦明が未入力')
            
        # タグ
        if request.form['tags']:
            tags = request.form['tags']
            tags = eval(tags)
            
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

        # サブファイルのINSERT(sellimgs_subの数分同じSellIDでINSERT)
        # if sellimgs_sub:
        #     for subimg in sellimgs_sub:
        #        subimg_sql = '''
        #        INSERT INTO SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}', {1}, b'0');
        #        '''.format(subimg, sellid)
        #        cursor.execute(subimg_sql)
    
        if images:
            for img in images:
               sellimg_insert = '''
               INSERT INTO SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}', {1}, 0);
               '''.format(img, sellid)
               cursor.execute(sellimg_insert)
        
        # サムネイルファイルのINSERT
        # mainimg_sql = '''
        # INSERT INTO 
        # SellIMG (SellIMG, SellID, ThumbnailFlg) VALUES ('{0}',{1},b'1');
        # '''.format(sellimg_main, sellid)
        # cursor.execute(mainimg_sql)
        thumbnail_update = '''
        UPDATE SellIMG 
        SET ThumbnailFlg = 1 
        WHERE SellIMG = '{0}' AND SellID = {1};
        '''.format(select,sellid)
        cursor.execute(thumbnail_update)
        print('実行:',thumbnail_update)
            
        # タグのINSERT
        if tags:
            for tag in tags:
                Tag_Insert = '''
                INSERT INTO Tag (Name, SellID) VALUE('{0}', {1});
                '''.format(tag,sellid)
                cursor.execute(Tag_Insert)
            
        # CLOSE
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('IndexPage'))
    
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
    
        layout_value = session.get('layout')
        print('layout:',layout_value)

        style = '''
            <style>
                *:not(input){{
                    color: {4} !important;
                }}
                html {{
                    background-color: {2} !important;
                }}
                .left-nav p {{
                    color: #000 !important;
                }}
                .right-nav ul li a, .right-nav ul li p{{
                    color: #000 !important;
                }}
                #btn{{
                    background-color: {0} !important;
                    color: {1} !important;
                }}
                footer {{
                    background-color: {5} !important;
                }}
                footer p{{
                    color: {6} !important;
                }}
                .which_btn02 {{
                    background-color: {3} !important;
                }}
            </style>
            '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
            
        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
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
        value = len(Account_Info)
    
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
            'pay_comp.html', Sell_Info=Sell_Info[0], Account_Info=Account_Info, icon=icon,
            UserName=UserName, Total_Price=Total_Price, SellID=SellID, After48H=After48H,
            After24H=After24H, style=style, layout_value=layout_value)

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
            
        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
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
            if SellerMoney is None:
                SellerMoney = int(0)
            
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
            return redirect(url_for('BuyCompPage', BuyID=BuyID, icon=icon, UserName=UserName))
        
        # 所持金が足りない
        else:
            error = True
            return redirect(url_for('ProductPage',sellid=SellID, error=error, icon=icon, UserName=UserName))

# /buycomp/<BuyID>
@app.route('/buycomp/<BuyID>')
def BuyCompPage(BuyID):
    conn = conn_db()
    cursor = conn.cursor()

    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)

    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
            .which_btn02 {{
                background-color: {3} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("buy_comp.html", MailAddress=MailAddress, 
                           style=style, layout_value=layout_value,
                           BuyID=BuyID, icon=icon, UserName=UserName)
    
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

# #########################################
# トップ
# #########################################

# /trend
@app.route('/trend')
def TrendPage():
    return render_template("trend.html")

# /index
@app.route('/')
def IndexPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    if you_list == None:
        return redirect(url_for('LoginPage'))
    
    if Admin(AccountID) == True:
        print('Admin:True')
        TablePage = True
    elif Admin(AccountID) == False:
        print('Admin:False')
        TablePage = False
    
    layout_value = session.get('layout')
    simple_value = list(session.get('simple'))
    slide_value = session.get('slideimg')
    print('layout:',layout_value)
    print('simple:',simple_value)
    print('slide:',slide_value)
    
    if simple_value[0] == 0:
        simple_value[0] = 'None'
    if simple_value[1] == 0:
        simple_value[1] = 'None'
    if simple_value[2] == 0:
        simple_value[2] = 'None'
    
    if layout_value != []:
        style = '''
            <style>
                *{{
                    color: {4} !important;
                }}
                html {{
                    background-color: {2} !important;
                }}
                .left-nav p {{
                    color: #000 !important;
                }}
                .right-nav ul li a, .right-nav ul li p{{
                    color: #000 !important;
                }}
                #btn{{
                    background-color: {0} !important;
                    color: {1} !important;
                }}
                footer {{
                    background-color: {5} !important;
                }}
                footer p{{
                    color: {6} !important;
                }}
                .slideshow .slide-content {{
                    color: {1} !important;
                }}
                .slideshow{{
                    display: {7} !important;
                }}
                .product img{{
                    display: {8} !important;
                }}
                .price-box{{
                    display: {9} !important;
                }}
            </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1], 
                   simple_value[0], simple_value[1], simple_value[2])
    else: 
        style = None
        slide_value = None

    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
    # 出品取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きではない。
    SellID_Select = '''
    SELECT Sell.SellID
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL 
    AND SellIMG.ThumbnailFlg = 0x01 
    AND Sell.Draft = 0x01 
    AND Sell.AccountID != {0};
    '''.format(AccountID)
    cursor.execute(SellID_Select)
    ids = cursor.fetchall()
    
    # シャッフル
    random.shuffle(ids)
    # top#10
    ids_top10 = ids[:10]
    # タプル
    ids_top10 = tuple(x[0] for x in ids_top10)
    ids_top10 = tuple(ids_top10)
    print(ids_top10)
    
    SellInfo_Select = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL 
    AND SellIMG.ThumbnailFlg = 0x01 
    AND Sell.Draft = 0x01 
    AND Sell.AccountID != {0} 
    AND Sell.SellID IN ({1})
    ORDER BY FIELD(Sell.SellID, {1});
    '''.format(AccountID,','.join(map(str, ids_top10)))
    print('実行:',SellInfo_Select)
    cursor.execute(SellInfo_Select)
    sells = cursor.fetchall()
    
    Search_Select = '''
    SELECT Word FROM Search
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Search_Select)
    words = list(cursor.fetchall())
    words = [word[0] for word in words]
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(
        "index.html", sells=sells, TablePage=TablePage, icon=icon, 
        UserName=UserName, style=style, layout_value=layout_value, 
        slide_value=slide_value,words=words)

# /product/<sellid>
@app.route('/product/<sellid>')
def ProductPage(sellid):
    error = request.args.get('error', None)
    conn = conn_db()
    cursor = conn.cursor()
    
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
        layout_value = session.get('layout')
        print('layout:',layout_value)

    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
            .btn05{{
                background-color: {3} !important
            }}
            .shopping form button{{
                background-color: {3} !important
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    myicon = cursor.fetchone()[0]
    
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
    
    # test-------------------------
    sql = '''
    select * from sell where SellID = {0};
    '''.format(sellid)
    cursor.execute(sql)
    record = cursor.fetchone()
    # -----------------------------
    
    # ブクマ済
    Nice_Select = '''
    SELECT * FROM Nice
    WHERE SellID = {0}
    AND AccountID = {1};
    '''.format(sellid,AccountID)
    cursor.execute(Nice_Select)
    if cursor.fetchone():
        nice = True
    else:
        nice = False
    
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
    
    # アイコンのSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(sell_acc[0])
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
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
    
    Tag_Select = '''
    SELECT Name FROM Tag
    WHERE SellID = {0};
    '''.format(sellid)
    cursor.execute(Tag_Select)
    tags = cursor.fetchall()
    tags = [item[0] for item in tags]
    
    Category_Select = '''
    SELECT SCategoryID FROM Scategory
    WHERE Name = '{0}';
    '''.format(products[0][3])
    print('実行:',Category_Select)
    cursor.execute(Category_Select)
    category_id = cursor.fetchone()[0]
    
    conn = conn_db()
    cursor = conn.cursor()
    
    # 出品取得のSELECT
    # 条件:購入がされていない、サムネイルがある、下書きではない。
    sells = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL 
    AND SellIMG.ThumbnailFlg = 0x01 
    AND Sell.Draft = 0x01 
    AND Sell.AccountID != {0} 
    AND Sell.ScategoryID = {1};
    '''.format(AccountID,category_id)
    print('実行:',sells)
    cursor.execute(sells)
    sells = cursor.fetchall()
    
    # CLOSE
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(
        "product.html",imgs=imgs, name=name, overview=overview, layout_value=layout_value,
        price=price, sellid=sellid, scategory=scategory, style=style, record=record,
        status=status, avg_evalate=avg_evalate, sell_acc=sell_acc, sells=sells, 
        error=error, tags=tags, icon=icon, myicon=myicon, UserName=UserName, nice=nice)
    
# /search
@app.route('/search', methods=['POST'])
def Search():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        layout_value = session.get('layout')
        simple_value = list(session.get('simple'))
    
        if simple_value[0] == 0:
            simple_value[0] = 'None'
        if simple_value[1] == 0:
            simple_value[1] = 'None'
        if simple_value[2] == 0:
            simple_value[2] = 'None'
        
        if layout_value != []:
            style = '''
                <style>
                    *{{
                        color: {4} !important;
                    }}
                    html {{
                        background-color: {2} !important;
                    }}
                    .left-nav p {{
                        color: #000 !important;
                    }}
                    .right-nav ul li a, .right-nav ul li p{{
                        color: #000 !important;
                    }}
                    #btn{{
                        background-color: {0} !important;
                        color: {1} !important;
                    }}
                    footer {{
                        background-color: {5} !important;
                    }}
                    footer p{{
                        color: {6} !important;
                    }}
                    .product img{{
                        display: {7} !important;
                    }}
                    .price-box{{
                        display: {8} !important;
                    }}
                </style>
            '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                       layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1], 
                       simple_value[1], simple_value[2])
        else: 
            style = None

        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
        search_word = request.form['search_word']
        print('ワード:',search_word)
        
        Sellname_Select = '''
        SELECT Sell.SellID, Sell.Name, Scategory.Name, Mcategory.Name, Tag.Name
        FROM Sell
        JOIN Scategory ON Sell.ScategoryID = Scategory.ScategoryID
        JOIN Mcategory ON Scategory.McategoryID = Mcategory.McategoryID
        JOIN Tag ON Tag.SellID = Sell.SellID
        WHERE Sell.AccountID <> {0}; 
        '''.format(AccountID)
        
        cursor.execute(Sellname_Select)
        sell_word = cursor.fetchall()
        
        sell_listInDict = []
        for item in sell_word:
            result_dict = {
                "ID": item[0],
                "Name": item[1],
                "S": item[2],
                "M": item[3],
                "Tag": item[4]
            }
            sell_listInDict.append(result_dict)
        
        hit_items = [item['ID'] for item in sell_listInDict if search_word 
                        in item['Name'] or search_word in item['S'] or search_word in item['M'] or search_word in item['Tag']]
        print('ヒットID:',hit_items)

        sells = []
        for id in hit_items:
            SellInfo_Select = '''
            SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
            FROM Sell
            JOIN SellIMG ON Sell.SellID = SellIMG.SellID
            LEFT JOIN Buy ON Sell.SellID = Buy.SellID
            WHERE SellIMG.ThumbnailFlg = 0x01 
            AND Sell.SellID = {0} 
            AND Buy.SellID IS NULL 
            AND Sell.Draft = 0x01;
            '''.format(id)
            print('実行:',SellInfo_Select)
            cursor.execute(SellInfo_Select)
            sellinfo = cursor.fetchone()
            if sellinfo != None:
                if sellinfo not in set(sells):
                    sells.append(sellinfo)
                
        if search_word:  # search_wordが空欄でない場合
            Search_Insert = '''
            INSERT INTO Search(Word, AccountID)
            VALUES('{0}', {1})
            '''.format(search_word, AccountID)
            cursor.execute(Search_Insert)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    return render_template('search.html',icon=icon,UserName=UserName,
                           sells=sells,search_word=search_word,style=style)

# /category_search
@app.route('/category_search',methods=['POST'])
def CateSearch():
    if request.method == 'POST':
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        
        layout_value = session.get('layout')
        simple_value = list(session.get('simple'))
    
        if simple_value[0] == 0:
            simple_value[0] = 'None'
        if simple_value[1] == 0:
            simple_value[1] = 'None'
        if simple_value[2] == 0:
            simple_value[2] = 'None'
        
        if layout_value != []:
            style = '''
                <style>
                    *{{
                        color: {4} !important;
                    }}
                    html {{
                        background-color: {2} !important;
                    }}
                    .left-nav p {{
                        color: #000 !important;
                    }}
                    .right-nav ul li a, .right-nav ul li p{{
                        color: #000 !important;
                    }}
                    #btn{{
                        background-color: {0} !important;
                        color: {1} !important;
                    }}
                    footer {{
                        background-color: {5} !important;
                    }}
                    footer p{{
                        color: {6} !important;
                    }}
                    .product img{{
                        display: {7} !important;
                    }}
                    .price-box{{
                        display: {8} !important;
                    }}
                </style>
            '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                       layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1], 
                       simple_value[1], simple_value[2])
        else: 
            style = None

        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
        select = request.form['select']
        print('select:',select)
        
        search_word = "カテゴリー名"
        
        sells = []
        SellInfo_Select = '''
        SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
        FROM Sell
        JOIN SellIMG ON Sell.SellID = SellIMG.SellID
        LEFT JOIN Buy ON Sell.SellID = Buy.SellID
        WHERE SellIMG.ThumbnailFlg = 0x01 
        AND Sell.ScategoryID = {0}
        AND Buy.SellID IS NULL 
        AND Sell.Draft = 0x01
        AND Sell.AccountID <> {1};
        '''.format(select,AccountID)
        print('実行:',SellInfo_Select)
        cursor.execute(SellInfo_Select)
        sells = list(cursor.fetchall())
        
        Category_Select = '''
        SELECT Name FROM Scategory
        WHERE ScategoryID = {0};
        '''.format(select)
        cursor.execute(Category_Select)
        search_word = cursor.fetchone()[0]
                
        Search_Insert = '''
        INSERT INTO Search(Word, AccountID)
        VALUES('{0}', {1})
        '''.format(search_word, AccountID)
        cursor.execute(Search_Insert)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    return render_template('search.html',icon=icon,UserName=UserName,style=style,
                           search_word=search_word,sells=sells)
    
# /data
@app.route("/data", methods=['POST'])
def get_data():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
        
    # フォームから送信されたデータを取得
    SellID = request.form['1']
    Name = request.form['2']
    Price = request.form['3']
    TaxID = request.form['4']
    PostageID = request.form['5']
    StatusID = request.form['6']
    Overview = request.form['7']
    ScategoryID = request.form['8']
    sell_AccountID = request.form['9']
    datetime = request.form['10']
    draft = request.form['11']
    
    # 取得したデータをカンマで区切った文字列にする
    # data_string = ','.join([SellID])
    data_string = ','.join([SellID, Name, Price, TaxID, PostageID, StatusID, Overview, ScategoryID, sell_AccountID, datetime, draft])
    
    Nice_Select = '''
    SELECT SellID FROM Nice
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Nice_Select)
    nice = cursor.fetchall()
    nices = [item[0] for item in nice]
    
    if int(SellID) not in nices:
        Nice_Insert = '''
        INSERT INTO Nice(AccountID, SellID)
        VALUES({0},{1});
        '''.format(AccountID,SellID)
        cursor.execute(Nice_Insert)
        print('実行:',Nice_Insert)
    else:
        Nice_Delete = '''
        DELETE FROM Nice
        WHERE AccountID = {0} AND SellID = {1};
        '''.format(AccountID,SellID)
        cursor.execute(Nice_Delete)
        print('実行:',Nice_Delete)
    
    conn.commit()
    cursor.close()
    conn.close()
    # 加工したデータをJSON形式で返す
    return jsonify({'data': data_string})


# #########################################
# マイページ
# #########################################
    
# /mypage
@app.route('/mypage')
def MyPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *:not(label,button,input){{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
            .bar {{
                background-color: {3} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    print('icon:',icon)
    
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
        UserName=UserName, avg_evalate=avg_evalate, icon=icon, 
        style=style, layout_value=layout_value)
    
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

# /favorite
@app.route('/favorite')
def FavoritePage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
        
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
    Nice_Select = '''
    SELECT SellID FROM Nice
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(Nice_Select)
    nice = cursor.fetchall()
    nices = [item[0] for item in nice]
    
    Sell_Select = '''
    SELECT Sell.SellID, Sell.Name, Sell.Price, SellIMG.SellIMG
    FROM Sell
    JOIN SellIMG ON Sell.SellID = SellIMG.SellID
    LEFT JOIN Buy ON Sell.SellID = Buy.SellID
    WHERE Buy.SellID IS NULL 
    AND SellIMG.ThumbnailFlg = 0x01
    AND Sell.SellID IN ({0});
    '''.format(','.join(map(str, nices)))
    cursor.execute(Sell_Select)
    print('実行:',Sell_Select)
    sellinfo = cursor.fetchall()
    print(sellinfo)
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template(
        "favorite.html", UserName=UserName, sellinfo=sellinfo,
        icon=icon, layout_value=layout_value, style=style)

# /viewlog
@app.route('/viewlog')
def ViewlogPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
        
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("viewlog.html", UserName=UserName, icon=icon,
                           style=style, layout_value=layout_value)

# /sell_list
@app.route('/sell_list')
def SellListPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
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
    return render_template('sell_list.html',Sells=Sells, icon=icon, UserName=UserName,
                           style=style, layout_value=layout_value)

# /buy_list
@app.route('/buy_list')
def BuyListPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
    
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('buy_list.html',icon=icon, UserName=UserName,
                           style=style, layout_value=layout_value)

# /savesearch
@app.route('/savesearch')
def SavesearchPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
        
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("saved_search.html", UserName=UserName, icon=icon,
                           style=style, layout_value=layout_value)
    
# /draft_list
@app.route('/draft_list')
def DraftPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
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
    return render_template('draft_list.html',Drafts=Drafts,icon=icon, UserName=UserName,
                           style=style, layout_value=layout_value)
        
# /personal
@app.route('/personal')
def PersonalPage():
    conn = conn_db()
    cursor = conn.cursor()
    
    # セッション取得
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    
    layout_value = session.get('layout')
    print('layout:',layout_value)
    
    style = '''
        <style>
            *{{
                color: {4} !important;
            }}
            html {{
                background-color: {2} !important;
            }}
            .left-nav p {{
                color: #000 !important;
            }}
            .right-nav ul li a, .right-nav ul li p{{
                color: #000 !important;
            }}
            #btn{{
                background-color: {0} !important;
                color: {1} !important;
            }}
            footer {{
                background-color: {5} !important;
            }}
            footer p{{
                color: {6} !important;
            }}
        </style>
        '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])
    
    # アイコンSELECT
    ProfIMG_Select = '''
    SELECT ProfIMG FROM Account
    WHERE AccountID = {0};
    '''.format(AccountID)
    cursor.execute(ProfIMG_Select)
    icon = cursor.fetchone()[0]
    
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
                           MailAddress=MailAddress, name_error=name_error, pass_error=pass_error, 
                           icon=icon, UserName=UserName, mail_error=mail_error,
                           style=style, layout_value=layout_value)
    
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

# /layout
@app.route('/layout',methods=['GET','POST'])
def LayoutPage():
        conn = conn_db()
        cursor = conn.cursor()
        
        # セッション取得
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        slide_value = session.get('slideimg')
        print('slide_value:',slide_value)
        ids = [slide_value[0][1],slide_value[1][1],slide_value[2][1],slide_value[3][1]]
        
        # アイコンSELECT
        ProfIMG_Select = '''
        SELECT ProfIMG FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(ProfIMG_Select)
        icon = cursor.fetchone()[0]
        
        if request.method == 'POST':
            # リセットの時
            if request.form['layout_action'] == 'reset':
                navbtn_color = '#ff0000'
                navtxt_color = '#ffffff'
                main_color = '#ff0000'
                wall_color = '#ffffff'
                text_color = '#000000'
                footer_color = '#000000'
                footertxt_color = '#ffffff'
                slideshow = '1'
                sellimg = '1'
                sellprice = '1'
                slideimg1 =  None
                slideimg2 =  None
                slideimg3 =  None
                slideimg4 =  None
                imgs = [
                    'static/images/slide/slide01.jpg', 'static/images/slide/slide05.jpg', 
                    'static/images/slide/slide08.jpg', 'static/images/slide/slide10.jpg'
                    ]
            # 入力内容保存の時
            elif request.form['layout_action'] == 'submit':
                navbtn_color = request.form['navbtn_color']
                navtxt_color = request.form['navtxt_color']
                main_color = request.form['main_color']
                wall_color = request.form['wall_color']
                text_color = request.form['text_color']
                footer_color = request.form['footer_color']
                footertxt_color = request.form['footertxt_color']
                slideshow = request.form['slideshow']
                sellimg = request.form['sellimg']
                sellprice = request.form['sellprice']
                
                # 画像保存
                upload_path = "static/images/slide/"
                imgs = []
                # 1
                slideimg1 = request.files.get('slideimg1')
                if slideimg1.filename == '':
                    slideimg1 = slide_value[0][0]
                    imgs.append(slideimg1)
                else:
                    img_path = os.path.join(upload_path, slideimg1.filename)
                    slideimg1.save(img_path)
                    imgs.append(img_path)
                # 2
                slideimg2 = request.files.get('slideimg2')
                if slideimg2.filename == '':
                    slideimg2 = slide_value[1][0]
                    imgs.append(slideimg2)
                else:
                    img_path = os.path.join(upload_path, slideimg2.filename)
                    slideimg2.save(img_path)
                    imgs.append(img_path)
                # 3
                slideimg3 = request.files.get('slideimg3')
                if slideimg3.filename == '':
                    slideimg3 = slide_value[2][0]
                    imgs.append(slideimg3)
                else:
                    img_path = os.path.join(upload_path, slideimg3.filename)
                    slideimg3.save(img_path)
                    imgs.append(img_path)
                # 4
                slideimg4 = request.files.get('slideimg4')
                if slideimg4.filename == '':
                    slideimg4 = slide_value[3][0]
                    imgs.append(slideimg4)
                else:
                    img_path = os.path.join(upload_path, slideimg4.filename)
                    slideimg4.save(img_path)
                    imgs.append(img_path)
                print('imgs:',imgs)
                
            # update
            for img,id in zip(imgs,ids):
                Slideimg_Update = '''
                UPDATE Numerical
                SET Numerical = '{0}'
                WHERE NumericalID = {1} AND AccountID = {2} ;
                '''.format(img,id,AccountID)
                cursor.execute(Slideimg_Update)
                print('実行:',Slideimg_Update)
                    
                
            # SQL アップデート
            NavBtnColor_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 1
            '''.format(navbtn_color, AccountID)
            cursor.execute(NavBtnColor_Update)
            print('実行:',NavBtnColor_Update)
            
            NavTxtColor_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 2
            '''.format(navtxt_color, AccountID)
            cursor.execute(NavTxtColor_Update)
            print('実行:',NavTxtColor_Update)
            
            WallColor_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 3
            '''.format(wall_color, AccountID)
            cursor.execute(WallColor_Update)
            print('実行:',WallColor_Update)
            
            MainColor_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 4
            '''.format(main_color, AccountID)
            cursor.execute(MainColor_Update)
            print('実行:',MainColor_Update)
            
            TextColor_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 5
            '''.format(text_color, AccountID)
            cursor.execute(TextColor_Update)
            print('実行:',TextColor_Update)
            
            Footer_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 6
            '''.format(footer_color, AccountID)
            cursor.execute(Footer_Update)
            print('実行:',Footer_Update)
            
            FooterTxt_Update = '''
            UPDATE Numerical
            SET Numerical = '{0}'
            WHERE AccountID = {1} AND LayoutID = 7
            '''.format(footertxt_color, AccountID)
            cursor.execute(FooterTxt_Update)
            print('実行:',FooterTxt_Update)
            
            Slideshow_Update = '''
            UPDATE Account
            SET SlideShowFlg = {0}
            WHERE AccountID = {1}
            '''.format(slideshow, AccountID)
            cursor.execute(Slideshow_Update)
            print('実行:',Slideshow_Update)
            
            SimpleThumb_Update = '''
            UPDATE Account
            SET SimpleThumbFlg = {0}
            WHERE AccountID = {1}
            '''.format(sellimg, AccountID)
            cursor.execute(SimpleThumb_Update)
            print('実行:',SimpleThumb_Update)
            
            SimplePrice_Update = '''
            UPDATE Account
            SET SimplePriceFlg = {0}
            WHERE AccountID = {1}
            '''.format(sellprice, AccountID)
            cursor.execute(SimplePrice_Update)
            print('実行:',SimplePrice_Update)
        
        # セッションへ入力
        Layout_Select = '''
        SELECT LayoutID, Numerical
        FROM Numerical
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(Layout_Select)
        print('実行:',Layout_Select)
        layout_value = cursor.fetchall()
        session['layout'] = layout_value
        
        Simple_Select = '''
        SELECT SlideShowFlg, SimpleThumbFlg, SimplePriceFlg
        FROM Account
        WHERE AccountID = {0};
        '''.format(AccountID)
        cursor.execute(Simple_Select)
        print('実行:',Simple_Select)
        simple_value = list(cursor.fetchone())
        session['simple'] = simple_value
        
        Slide_Select = '''
        SELECT Numerical, NumericalID 
            FROM Numerical
            WHERE AccountID = {0} 
            AND LayoutID IN (8, 9, 10, 11);
            '''.format(AccountID)
        cursor.execute(Slide_Select)
        print('実行:',Slide_Select)
        slide_value = cursor.fetchall()
        session['slideimg'] = slide_value

        # スタイルタグ
        style = '''
            <style>
                * {{
                    color: {4} !important;
                }}
                html {{
                    background-color: {2} !important;
                }}
                .left-nav p {{
                    color: #000 !important;
                }}
                .right-nav ul li a, .right-nav ul li p{{
                    color: #000 !important;
                }}
                #btn{{
                    background-color: {0} !important;
                    color: {1} !important;
                }}
                .which_btn02{{
                    background-color: {3} !important;
                }}
                footer {{
                    background-color: {5} !important;
                }}
                footer p{{
                    color: {6} !important;
                }}
            </style>
            '''.format(layout_value[0][1], layout_value[1][1], layout_value[2][1], 
                   layout_value[3][1], layout_value[4][1], layout_value[5][1], layout_value[6][1])

        conn.commit()
        cursor.close()
        conn.close()
        return render_template('layout.html', UserName=UserName, icon=icon, style=style, 
                               layout_value=layout_value, simple_value=simple_value)

# /logout
@app.route('/logout')
def Logout():
    session['you'] = None
    return redirect(url_for('LoginPage'))

# #########################################
# 管理者
# #########################################

# 管理者チェック
def Admin(AccountID):
    if AccountID == 1:
        return True
    else:
        return False

# /table
@app.route('/table', methods=['GET', 'POST'])
def TablePage():
    you_list = session.get('you')
    if you_list:
        AccountID, UserName, MailAddress = you_list[0]
    if Admin(AccountID) == True:
        print('Admin:True')
    elif Admin(AccountID) == False:
        print('Admin:False')
        return redirect(url_for('IndexPage'))
    
    return render_template('table.html')

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
                # "TableID": request.form['TableID'],
                "AccountID": request.form['AcID'],
                "SellID": request.form['SellID'],
                "Content": request.form['Content']
                # "Datetime": request.form['Datetime']
            }
        
        elif TableName == 'Layout':
            inputs = {
                # "TableID": request.form['TableName'],
                "Name": request.form['Name']
            }
        
        elif TableName == 'Mcategory':
            inputs = {
                # "McategoryID": request.form['TableID'],
                "Name": request.form['Name']
            }
            
        elif TableName == 'Nice':
            inputs = {
                # "TableID": request.form['TableID'],
                "AccountID": request.form['AcID'],
                "SellID": request.form['SellID']
            }
            
        elif TableName == 'Numerical':
            inputs = {
                # "tableIDID": request.form['TableID'],
                "Numerical": request.form['Numerical'],
                "LayoutID": request.form['LayoutID'],
                "AccountID": request.form['AcID']
            }
            
        elif TableName == 'Postage':
            inputs = {
                # "TableID": request.form['TableID'],
                "Size": request.form['Size'],
                "Price": request.form['Price'],
            }
            
        elif TableName == 'Reply':
            inputs = {
                # "TableID": request.form['TableID'],
                "ChatID": request.form['ChatID'],
                "Content": request.form['Content']
                # "Datetime": request.form['Datetime']
            }
            
        elif TableName == 'Scategory':
            inputs = {
                # "TableID": request.form['TableID'],
                "Name": request.form['Name'],
                "McategoryID": request.form['McategoryID']
            }
            
        elif TableName == 'Search':
            inputs = {
                # "TableID": request.form['TableID'],
                "Word": request.form['Word'],
                "AccountID": request.form['AcID']
            }
            
        elif TableName == 'Sell':
            inputs = {
                # "TableID": request.form['TableID'],
                "Name": request.form['Name'],
                "Price": request.form['Price'],
                "TaxID": request.form['TaxID'],
                "PostageID": request.form['PostageID'],
                "StatusID": request.form['StatusID'],
                "Overview": request.form['Overview'],
                "ScategoryID": request.form['ScategoryID'],
                "AccountID": request.form['AcID'],
                # "Datetime": request.form['Datetime'],
                "draft": int(request.form['draft'])
            }
            
        elif TableName == 'SellIMG':
            inputs = {
                # "TableID": request.form['TableID'],
                "SellIMG": request.form['SellIMG'],
                "ThumbnailFlg": int(request.form['ThumbnailFlg']),
                "SellID": request.form['SellID']
            }
            
        elif TableName == 'Sex':
            inputs = {
                # "TableID": request.form['TableID'],
                "Sex": request.form['Sex']
            }
            
        elif TableName == 'Status':
            inputs = {
                # "TableID": request.form['TableID'],
                "Name": request.form['Name']
            }
            
        elif TableName == 'Tag':
            inputs = {
                # "TableID": request.form['TableID'],
                "Name": request.form['Name'],
                "SellID": request.form['SellID']
            }
            
        elif TableName == 'Tax':
            inputs = {
                # "TableID": request.form['TableID'],
                "Section": request.form['Section'],
                "Tax": request.form['Tax']
            }
            
        elif TableName == 'View':
            inputs = {
                # "TableID": request.form['TableID'],
                "AccountID": request.form['AcID'],
                "SellID": request.form['SellID']
            }
        
        else:
            return '予期しない TableName'
            
        # 辞書型のキー
        RowNames = ', '.join(inputs.keys())
        # 辞書型のデータ × length
        RowDatas = ', '.join(['%s'] * len(inputs))
        print(list(inputs.values()))
            
        if btn_value == 'insert':
            Row_Insert = '''
            INSERT INTO {0} ({1}) VALUES ({2});
            '''.format(TableName,RowNames,RowDatas)
            #                          ↓ RowDatas 
            print('実行:',Row_Insert)
            cursor.execute(Row_Insert, list(inputs.values()))
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
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
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
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Sex'
        cursor.execute("SELECT * FROM Sex")
        Sex = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Sex.html', Sex=Sex,TableName=TableName)

# /DB_Address
@app.route('/DB_Address', methods=['GET', 'POST'])
def DB_Address():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Address'
        cursor.execute("SELECT * FROM Address")
        Address = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Address.html', Address=Address,TableName=TableName)

# /DB_Sell
@app.route('/DB_Sell', methods=['GET', 'POST'])
def DB_Sell():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Sell'
        cursor.execute("SELECT * FROM Sell")
        Sell = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Sell.html', Sell=Sell,TableName=TableName)

# /DB_SellIMG
@app.route('/DB_SellIMG', methods=['GET', 'POST'])
def DB_SellIMG():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'SellIMG'
        cursor.execute("SELECT * FROM SellIMG")
        SellIMG = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_SellIMG.html', SellIMG=SellIMG,TableName=TableName)

# /DB_Status
@app.route('/DB_Status', methods=['GET', 'POST'])
def DB_Status():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Status'
        cursor.execute("SELECT * FROM Status")
        Status = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Status.html', Status=Status,TableName=TableName)

# /DB_Mcategory
@app.route('/DB_Mcategory', methods=['GET', 'POST'])
def DB_Mcategory():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Mcategory'
        cursor.execute("SELECT * FROM Mcategory")
        Mcategory = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Mcategory.html', Mcategory=Mcategory,TableName=TableName)

# /DB_Scatgeory
@app.route('/DB_Scategory', methods=['GET', 'POST'])
def DB_Scategory():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Scategory'
        cursor.execute("SELECT * FROM Scategory")
        Scategory = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Scategory.html', Scategory=Scategory,TableName=TableName)

# /DB_Tag
@app.route('/DB_Tag', methods=['GET', 'POST'])
def DB_Tag():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Tag'
        cursor.execute("SELECT * FROM Tag")
        Tag = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Tag.html', Tag=Tag,TableName=TableName)

# /DB_Buy
@app.route('/DB_Buy', methods=['GET', 'POST'])
def DB_Buy():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Buy'
        cursor.execute("SELECT * FROM Buy")
        Buy = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Buy.html', Buy=Buy,TableName=TableName)

# /DB_Nice
@app.route('/DB_Nice', methods=['GET', 'POST'])
def DB_Nice():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Nice'
        cursor.execute("SELECT * FROM Nice")
        Nice = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Nice.html', Nice=Nice,TableName=TableName)

# /DB_View
@app.route('/DB_View', methods=['GET', 'POST'])
def DB_View():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'View'
        cursor.execute("SELECT * FROM View")
        View = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_View.html', View=View,TableName=TableName)

# /DB_chat
@app.route('/DB_Chat', methods=['GET', 'POST'])
def DB_Chat():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Chat'
        cursor.execute("SELECT * FROM Chat")
        Chat = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Chat.html', Chat=Chat,TableName=TableName)

# /DB_Tax
@app.route('/DB_Tax', methods=['GET', 'POST'])
def DB_Tax():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Tax'
        cursor.execute("SELECT * FROM Tax")
        Tax = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Tax.html', Tax=Tax,TableName=TableName)

# /DB_Postage
@app.route('/DB_Postage', methods=['GET', 'POST'])
def DB_Postage():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Postage'
        cursor.execute("SELECT * FROM Postage")
        Postage = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Postage.html', Postage=Postage,TableName=TableName)

# /DB_Reply
@app.route('/DB_Reply', methods=['GET', 'POST'])
def DB_Reply():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Reply'
        cursor.execute("SELECT * FROM Reply")
        Reply = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Reply.html', Reply=Reply,TableName=TableName)

# /DB_Layout
@app.route('/DB_Layout', methods=['GET', 'POST'])
def DB_Layout():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Layout'
        cursor.execute("SELECT * FROM Layout")
        Layout = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Layout.html', Layout=Layout,TableName=TableName)

# /DB_Numerical
@app.route('/DB_Numerical', methods=['GET', 'POST'])
def DB_Numerical():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
        TableName = 'Numerical'
        cursor.execute("SELECT * FROM Numerical")
        Numerical = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('DB_Numerical.html', Numerical=Numerical,TableName=TableName)

# /DB_Search
@app.route('/DB_Search', methods=['GET', 'POST'])
def DB_Search():
        conn = conn_db()
        cursor = conn.cursor()
        
        you_list = session.get('you')
        if you_list:
            AccountID, UserName, MailAddress = you_list[0]
        if Admin(AccountID) == True:
            print('Admin:True')
        elif Admin(AccountID) == False:
            print('Admin:False')
            return redirect(url_for('IndexPage'))
        
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