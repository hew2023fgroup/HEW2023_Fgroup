from flask import Flask , render_template , request ,url_for , redirect
import mysql.connector #mysql-connector-python読み込む

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
app = Flask(__name__)
#db接続
def conn_db():
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root" ,
        passwd="P@ssw0rd",
        db ="hew"
    )
    return conn
#manageuserで表示する,情報をselect取り出し
@app.route("/manageuser")
def userdelete():
    conn = conn_db()
    cursor = conn.cursor()
    sql = "select * from account"
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template("manageuser.html", records=result)

#削除するとき
@app.route("/delete/",methods=["GET"])
def user_delete():
    conn=""
    cursor=""
    
    try:
        id = request.args.get("id","")
        conn=conn_db()
        cursor = conn.cursor()
        #id(0の値)を消す
        sql = "delete from account where AccountID={0};".format(id)
        cursor.execute(sql)
        conn.commit()
#例外
    except mysql.connector.ProgrammingError as e:
        print(e)
        
    finally:
        if cursor !="":
            cursor.close()
            
        if conn.connection_id !="":
            conn.close()
            
    return render_template(url_for("manageuser.html"))