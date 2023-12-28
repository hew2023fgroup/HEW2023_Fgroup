#出品,下書き時のデータ格納と一覧ページの表示(/sell,/sell/→sell.pyから引用,sql変更有)
from flask import Flask, redirect, url_for, render_template, request,session
import mysql.connector
import os

#pychach
import sys
sys.dont_write_bytecode = True

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

# 出品ページ確認用------------------------------------------------------------
@app.route('/index')
def IndexPage():
    return render_template("index.html")
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
        
# /sell
@app.route('/sell')
def SellPage():
    # セッションから取り出す(結合するときにコメントアウトを外す)
    # you_list = session.get('you')
    # if you_list:
    #     AccountID, UserName, MailAddress = you_list[0]
    #     print(UserName, "でログイン中")
    return render_template("sell.html")

# /sell/
@app.route('/sell/', methods=['POST'])
def Sell():    
    if request.method == 'POST':
        # (結合するときにコメントアウトを外す)
        # you_list = session.get('you')
        # if you_list:
        #     AccountID, UserName, MailAddress = you_list[0]
        
        # 結合後削除!!!!!!!
        AccountID = 1
        
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
        if request.form['comp'] == "出品する":
        # 出品時のsql、boolは0
            sell = '''
                INSERT INTO Sell 
                (Name, Price, PostageID, StatusID, Overview, SCategoryID, AccountID,bool) 
                VALUES ('{0}',{1},{2},{3},'{4}',{5},{6},0);
               '''.format(selltit,price,postage,status,overview,scategoryid,AccountID)
               
        elif request.form['comp'] == "下書きに保存する":
        # 下書き時のsql,boolは1
            sell = '''
                INSERT INTO Sell 
                (Name, Price, PostageID, StatusID, Overview, SCategoryID, AccountID,bool) 
                VALUES ('{0}',{1},{2},{3},'{4}',{5},{6},1);
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
        
        return render_template('mypage.html')
