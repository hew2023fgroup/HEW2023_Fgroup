
## ルール追加(以降はここに記していきます)
* ルート関数の一行上にはそのルート関数の機能概要をコメントアウトする
* flaskのルート関数と同じ行に一度タブを入れてそのルート関数の作成者の名前をコメントアウトで記述する<br>
(例↓)
```python
# index.htmlの表示
@app.route("/")	# 岡郁也
def index():
	return render_template("index.html")
```

## マージ後は全員必ず「git pull origin develop」で作業環境の更新を行う<br>
→作業中に誰かのプルリクがマージされたときはpullを行ってからプッシュをする

## ブランチの種類
* mainブランチ：本番環境。マージのみでプッシュしない
* developブランチ：開発環境。基本的にはマージのみでプッシュしない
* feature/#issue番号：各々が作業するブランチ

コミット内容は1メッセージに書き込める内容にとどめる
	→ブランチを多めに作ることで後戻りをしやすくする

## 気を付けること
* 同じファイルを複数の人に作業させない
	コンフリクトが起こる
	→一機能一ファイル作成
		→ マージ → 複数の機能ファイルを最終的に一つにまとめる
* プルリクエストからマージした後は全員git pull origin ブランチ名で作業環境の更新を行う
	プッシュ前にdevelopの更新を確認

VSCodeでGitの運用ができます。こんがらがっても対応はしませんが、かなり楽になるので挑戦したい人は以下のURLからどうぞ
https://qiita.com/y-tsutsu/items/2ba96b16b220fb5913be

# githubの運用方法(<font color="Red">！</font>は一度行ったら次回以降行う必要なし)
## 1.ローカルリポジトリの作成(リモートリポジトリから自分で作成する場合)
<font color="Red">！</font>作業したい場所にフォルダを作り、ディレクトリ内に遷移
```bash
mkdir <フォルダ名>
```
```bash
cd <さっき作ったフォルダのディレクトリ>
```
<font color="Red">！</font>ローカルリポジトリの作成
```bash
git init

Initialized empty Git repository in ~
```
## 2.リモートリポジトリの環境をクローンする(既にリモートリポジトリがある場合はここから)
<font color="Red">！</font>作業環境をクローンする
```bash
git clone <リモートリポジトリのurl>
```
## 3.作業
作業ブランチを作成
```bash
git branch <ブランチ名>
```
作業ブランチに移動
```bash
git checkout <ブランチ名>
```

～～作業～～

indexに作業履歴を登録
```bash
git add <ファイル名>
```
## 4.作業後
indexに登録してある作業履歴をコミットとしてまとめて登録
```bash
git commit -m "コミットコメント"
```
## 5.リモートリポジトリにプッシュ
<font color="Red">！</font>リモートリポジトリをローカルリポジトリと紐づける
```bash
git remote add origin <リモートリポジトリのurl>
```
プッシュ前に作業環境の更新がないかを確認<br>
→作業環境(develop)の更新がある場合は作業環境を更新
```bash
git pull origin develop
```
commitに登録した変更処理をリモートリポジトリに反映する

```bash
git push origin <ブランチ名>

Counting objects: 3, done.
Writing objects: 100% (3/3), 245 bytes | 245.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To https://github.com/abcde/push_any.git
* [new branch]      main -> main
```
上記の表示が出たらプッシュ成功
## 6.プルリクエストからマージまで
githubにプッシュ後はプルリクエストを行う<br>
管理者がプルリクエストを受けてdevelopへのマージを行う<br>