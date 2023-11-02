githubの運用方法(*は一度行ったら次回以降行う必要なし)
	1.ローカルリポジトリの作成
		*作業したい場所にフォルダを作る
		gitからcdコマンドで作成したフォルダのディレクトリに遷移する
		*「git init」でローカルリポジトリの作成 → 「Initialized empty Git repository in ~」と表示されれば成功
	2.リモートリポジトリの環境をクローンする
		*「git clone リモートリポジトリのurl」で作業環境をクローンする
	3.作業
		「git branch ブランチ名」でブランチを作成
		「git checkout ブランチ名」で指定したブランチに移動
		「git add ファイル名」でindexにファイルを登録
	4.作業後
		「git commit -m "コミットコメント"」でgitに変更した処理を登録
	5.リモートリポジトリにプッシュ
		*「git remote add origin リモートリポジトリのurl」でリモートリポジトリをgitに追加
		プッシュ前に作業環境の更新がないかを確認。なければ次へ
			→作業環境(develop)の更新があった場合は「git pull develop」で作業環境を更新
		「git push origin ブランチ名」でcommitに登録した変更処理をリモートリポジトリに反映する
			→	Counting objects: 3, done.
				Writing objects: 100% (3/3), 245 bytes | 245.00 KiB/s, done.
				Total 3 (delta 0), reused 0 (delta 0)
				To https://github.com/abcde/push_any.git
 				* [new branch]      master -> master
 				上記の表示が出たらプッシュ成功
 	7.プルリクエストからマージまで
 		githubにプッシュ後はプルリクエストを行う
 		管理者がプルリクエストを受けてdevelopへのマージを行う
 		マージ後は全員必ず「git pull origin develop」で作業環境の更新を行う
 			→作業中に誰かのプルリクがマージされたときはpullを行ってからプッシュをする

ブランチの種類
	masterブランチ：本番環境。マージのみでプッシュしない
	developブランチ：開発環境。基本的にはマージのみでプッシュしない
	feature/#issue番号：各々が作業するブランチ

コミット内容は1メッセージに書き込める内容にとどめる
	→ブランチを多めに作ることで後戻りをしやすくする

気を付けること
・同じファイルを複数の人に作業させない
	コンフリクトが起こる
	→一機能一ファイル作成
		→ マージ → 複数の機能ファイルを最終的に一つにまとめる
・プルリクエストからマージした後は全員git pull origin ブランチ名で作業環境の更新を行う
	プッシュ前にdevelopの更新を確認

VSCodeでGitの運用ができます。こんがらがっても対応はしませんが、かなり楽になるので挑戦したい人は以下のURLからどうぞ
https://qiita.com/y-tsutsu/items/2ba96b16b220fb5913be