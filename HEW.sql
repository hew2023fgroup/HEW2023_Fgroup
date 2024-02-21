CREATE DATABASE HEW;
use HEW;

CREATE TABLE `Account` (
  `AccountID` int PRIMARY KEY AUTO_INCREMENT,
  `UserName` varchar(255),
  `Password` varchar(255),
  `ProfIMG` varchar(255),
  `Birthday` date,
  `SexID` int,
  `MailAddress` varchar(255),
  `KanjiName` varchar(255),
  `Furigana` varchar(255),
  `RegistDate` datetime DEFAULT (now()),
  `Money` int,
  `SimpleThumbFlg` bit(1) DEFAULT 1,
  `SimplePriceFlg` bit(1) DEFAULT 1,
  `SlideShowFlg` bit(1) DEFAULT 1
);

CREATE TABLE `Sex` (
  `SexID` int PRIMARY KEY AUTO_INCREMENT,
  `Sex` varchar(6)
);

CREATE TABLE `Address` (
  `AddressID` int PRIMARY KEY AUTO_INCREMENT,
  `Address` varchar(1000),
  `POST` varchar(8),
  `AccountID` int
);

CREATE TABLE `Sell` (
  `SellID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Price` int,
  `TaxID` int,
  `PostageID` int,
  `StatusID` int,
  `Overview` varchar(2000),
  `ScategoryID` int,
  `AccountID` int,
  `Datetime` datetime DEFAULT (now()),
  `draft` bit(1) DEFAULT 1
);

CREATE TABLE `SellIMG` (
  `SellIMGID` int PRIMARY KEY AUTO_INCREMENT,
  `SellIMG` varchar(2000),
  `ThumbnailFlg` bit(1) DEFAULT 1,
  `SellID` int
);

CREATE TABLE `Status` (
  `StatusID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255)
);

CREATE TABLE `Mcategory` (
  `McategoryID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255)
);

CREATE TABLE `Scategory` (
  `ScategoryID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `McategoryID` int
);

CREATE TABLE `Tag` (
  `TagID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `SellID` int
);

CREATE TABLE `Buy` (
  `BuyID` int PRIMARY KEY AUTO_INCREMENT,
  `SellID` int,
  `AccountID` int,
  `Review` int,
  `Datetime` datetime DEFAULT (now())
);

CREATE TABLE `Nice` (
  `NiceID` int PRIMARY KEY AUTO_INCREMENT,
  `AccountID` int,
  `SellID` int
);

CREATE TABLE `View` (
  `ViewID` int PRIMARY KEY AUTO_INCREMENT,
  `AccountID` int,
  `SellID` int
);

CREATE TABLE `Chat` (
  `ChatID` int PRIMARY KEY AUTO_INCREMENT,
  `AccountID` int,
  `SellID` int,
  `Content` varchar(2000),
  `Datetime` datetime DEFAULT (now())
);

CREATE TABLE `Tax` (
  `TaxID` int PRIMARY KEY AUTO_INCREMENT,
  `Section` varchar(255),
  `Tax` int
);

CREATE TABLE `Postage` (
  `PostageID` int PRIMARY KEY AUTO_INCREMENT,
  `Size` varchar(2),
  `Price` int
);

CREATE TABLE `Reply` (
  `ReplyID` int PRIMARY KEY AUTO_INCREMENT,
  `ChatID` int,
  `Content` varchar(2000),
  `Datetime` datetime DEFAULT (now())
);

CREATE TABLE `Layout` (
  `LayoutID` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255)
);

CREATE TABLE `Numerical` (
  `NumericalID` int PRIMARY KEY AUTO_INCREMENT,
  `Numerical` varchar(255),
  `LayoutID` int,
  `AccountID` int
);

CREATE TABLE `Search` (
  `SearchID` int PRIMARY KEY AUTO_INCREMENT,
  `Word` varchar(255),
  `AccountID` int
);

ALTER TABLE `Account` ADD FOREIGN KEY (`SexID`) REFERENCES `Sex` (`SexID`);

ALTER TABLE `Address` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Sell` ADD FOREIGN KEY (`TaxID`) REFERENCES `Tax` (`TaxID`);

ALTER TABLE `Sell` ADD FOREIGN KEY (`PostageID`) REFERENCES `Postage` (`PostageID`);

ALTER TABLE `Sell` ADD FOREIGN KEY (`StatusID`) REFERENCES `Status` (`StatusID`);

ALTER TABLE `Sell` ADD FOREIGN KEY (`ScategoryID`) REFERENCES `Scategory` (`ScategoryID`);

ALTER TABLE `Sell` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `SellIMG` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `Scategory` ADD FOREIGN KEY (`McategoryID`) REFERENCES `Mcategory` (`McategoryID`);

ALTER TABLE `Tag` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `Buy` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Nice` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Nice` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `View` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `View` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `Chat` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Chat` ADD FOREIGN KEY (`SellID`) REFERENCES `Sell` (`SellID`);

ALTER TABLE `Reply` ADD FOREIGN KEY (`ChatID`) REFERENCES `Chat` (`ChatID`);

ALTER TABLE `Numerical` ADD FOREIGN KEY (`LayoutID`) REFERENCES `Layout` (`LayoutID`);

ALTER TABLE `Numerical` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

ALTER TABLE `Search` ADD FOREIGN KEY (`AccountID`) REFERENCES `Account` (`AccountID`);

INSERT INTO Sex(Sex) VALUES("男");
INSERT INTO Sex(Sex) VALUES("女");
INSERT INTO Sex(Sex) VALUES("秘密");

INSERT INTO Status(Name) VALUES("新品、未使用");
INSERT INTO Status(Name) VALUES("未使用に近い");
INSERT INTO Status(Name) VALUES("目立った傷・汚れなし");
INSERT INTO Status(Name) VALUES("やや傷汚れあり");
INSERT INTO Status(Name) VALUES("傷や汚れあり");
INSERT INTO Status(Name) VALUES("全体的に状態が悪い");

INSERT INTO Tax(Section,Tax) VALUES("課税対象",10);

INSERT INTO Postage(Size,Price) VALUES("大",1650);
INSERT INTO Postage(Size,Price) VALUES("中",1350);
INSERT INTO Postage(Size,Price) VALUES("小",1060);

INSERT INTO Mcategory(Name) VALUES("レディース");
INSERT INTO Mcategory(Name) VALUES("メンズ");
INSERT INTO Mcategory(Name) VALUES("ベビー・キッズ");
INSERT INTO Mcategory(Name) VALUES("インテリア・住まい・小物");
INSERT INTO Mcategory(Name) VALUES("本・音楽・ゲーム");
INSERT INTO Mcategory(Name) VALUES("おもちゃ・ホビー・グッズ");
INSERT INTO Mcategory(Name) VALUES("コスメ・香水・美容");
INSERT INTO Mcategory(Name) VALUES("家電・スマホ・カメラ");
INSERT INTO Mcategory(Name) VALUES("スポーツ・レジャー");
INSERT INTO Mcategory(Name) VALUES("ハンドメイド");
INSERT INTO Mcategory(Name) VALUES("チケット");
INSERT INTO Mcategory(Name) VALUES("その他");

INSERT INTO Scategory(Name,McategoryID) VALUES("トップス",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("トップス",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("パンツ",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("パンツ",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("シューズ",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("シューズ",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("バッグ",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("バッグ",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("アクセサリー",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("アクセサリー",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("ファッション小物",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("ファッション小物",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("ベビー服",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("キッズ服",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("キッズシューズ",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("子供用ファッション小物",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("キッチン・食器",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("家具・収納",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("カーペット",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("カーテン",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("ライト",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("インテリア小物",4);
INSERT INTO Scategory(Name,McategoryID) VALUES("本",5);
INSERT INTO Scategory(Name,McategoryID) VALUES("CD",5);
INSERT INTO Scategory(Name,McategoryID) VALUES("DVD",5);
INSERT INTO Scategory(Name,McategoryID) VALUES("テレビゲーム",5);
INSERT INTO Scategory(Name,McategoryID) VALUES("おもちゃ",6);
INSERT INTO Scategory(Name,McategoryID) VALUES("コミック・アニメグッズ",6);
INSERT INTO Scategory(Name,McategoryID) VALUES("楽器・機材",6);
INSERT INTO Scategory(Name,McategoryID) VALUES("コスメ",7);
INSERT INTO Scategory(Name,McategoryID) VALUES("香水",7);
INSERT INTO Scategory(Name,McategoryID) VALUES("スキンケア",7);
INSERT INTO Scategory(Name,McategoryID) VALUES("ヘアケア",7);
INSERT INTO Scategory(Name,McategoryID) VALUES("ボディケア",7);
INSERT INTO Scategory(Name,McategoryID) VALUES("スマートフォン",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("PC",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("カメラ",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("テレビ",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("オーディオ",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("生活家電",8);
INSERT INTO Scategory(Name,McategoryID) VALUES("ゴルフ",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("釣り",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("野球",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("サッカー",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("テニス",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("スノーボード",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("アウトドア",9);
INSERT INTO Scategory(Name,McategoryID) VALUES("アクセサリー",10);
INSERT INTO Scategory(Name,McategoryID) VALUES("ファッション・小物",10);
INSERT INTO Scategory(Name,McategoryID) VALUES("時計",10);
INSERT INTO Scategory(Name,McategoryID) VALUES("インテリア",10);
INSERT INTO Scategory(Name,McategoryID) VALUES("音楽",11);
INSERT INTO Scategory(Name,McategoryID) VALUES("スポーツ",11);
INSERT INTO Scategory(Name,McategoryID) VALUES("演劇",11);
INSERT INTO Scategory(Name,McategoryID) VALUES("映画",11);
INSERT INTO Scategory(Name,McategoryID) VALUES("優待券",11);
INSERT INTO Scategory(Name,McategoryID) VALUES("ペット用品",12);
INSERT INTO Scategory(Name,McategoryID) VALUES("食品",12);
INSERT INTO Scategory(Name,McategoryID) VALUES("日用品",12);
INSERT INTO Scategory(Name,McategoryID) VALUES("事務用品",12);
INSERT INTO Scategory(Name,McategoryID) VALUES("その他",12);

INSERT INTO Account(UserName,Password,Birthday,SexID,MailAddress,KanjiName,Furigana,Money) VALUES("hogehoge","P@ssw0rd","2001-01-01",1,"sample@gmail.com","HAL太郎","ハルタロウ",3000);
INSERT INTO Account(UserName,Password,Birthday,SexID,MailAddress,KanjiName,Furigana,Money) VALUES("test","P@ssw0rd","2011-02-02",2,"sample_test@gmail.com","テスト太郎","テストタロウ",5000);
INSERT INTO Account(UserName,Password,Birthday,SexID,MailAddress,KanjiName,Furigana,Money) VALUES("test2","P@ssw0rd","2000-08-10",1,"sample_test2@gmail.com","近藤雅仁","コンドウマサト",2000);

INSERT INTO Address(Address,POST,AccountID) VALUES("愛知県名古屋市中村区名駅4-27-1HAL名古屋","450-0002",1);
INSERT INTO Address(Address,POST,AccountID) VALUES("福島県本宮市本宮雲雀田","349-7",1);
INSERT INTO Address(Address,POST,AccountID) VALUES("青森県むつ市脇野沢赤坂","790-17",2);
INSERT INTO Address(Address,POST,AccountID) VALUES("岡山県新見市神郷下神代","901-15",3);

INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("Sample商品データ",2000,1,2,2,"サンプルデータです。最終的には削除するデータです。",6,1,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("PS5",6000,1,1,1,"使ってたPS5なんですけど使わなくなったので売ります",26,1,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("コナン缶バッジ",800,1,3,2,"被ったので一枚どうですか？",28,1,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("お弁当箱",1500,1,3,1,"自作のお弁当箱どうですか？",17,1,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("マリオメーカー2",3000,1,3,2,"接続不良なし",26,1,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("缶バッジ アスナ",1800,1,3,1,"誰か欲しい人どうぞ",28,2,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("ディズニー 帽子",3000,1,3,3,"娘のおさがりでよければだれか買ってくれませんか？",16,2,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("アスナの缶バッジ",2000,1,3,1,"未開封です。",28,2,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("キリトの缶バッジ",2000,1,3,2,"未開封です。",28,2,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("SAO缶バッジセット",2500,1,3,1,"アリシゼーション仲良し組です",28,2,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("シノンのイラスト色紙",3000,1,3,2,"一度は言ってみたい武器名ランキング第一位、ウルティマラティオへカートⅡ",28,3,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("自作バッグ",5000,1,2,1,"バッグ作ってみました。どうですか？",7,3,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("スタバ タンブラー",3000,1,2,2,"使ってましたがちゃんと洗いました。",17,3,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("タンブラー 幽霊",3000,1,2,1,"未使用です",17,3,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("チップとデールのタンブラー",3400,1,2,2,"使わなくなったので売りたいと思います。",17,3,1);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("SAO色紙",3000,1,3,1,"SAO最高！",28,1,0);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("SAOプログレッシブ第五巻",1300,1,3,2,"読み終えたので誰か欲しい人に売ります。",23,2,0);
INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("SAOプログレッシブ第四巻",1300,1,3,2,"読み終わったのでだれかどうですか？",23,3,0);

INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/Product (1).jpeg",1);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample.png",2);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample01.png",3);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample02.png",4);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample03.png",5);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample04.png",6);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample05.png",7);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample06.png",8);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample07.png",9);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample08.png",10);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/sample09.png",11);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/pro_detail01.jpg",12);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo06.png",13);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo08.png",14);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo09.png",15);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo01.png",16);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo04.png",17);
INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/saved-photo05.png",18);

INSERT INTO Layout(Name) VALUES("navボタン色");
INSERT INTO Layout(Name) VALUES("nav文字色");
INSERT INTO Layout(Name) VALUES("main背景色");
INSERT INTO Layout(Name) VALUES("mainボタン色");
INSERT INTO Layout(Name) VALUES("main文字色");
INSERT INTO Layout(Name) VALUES("footer背景色");
INSERT INTO Layout(Name) VALUES("footer文字色");
INSERT INTO Layout(Name) VALUES("スライドショー画像1");
INSERT INTO Layout(Name) VALUES("スライドショー画像2");
INSERT INTO Layout(Name) VALUES("スライドショー画像3");
INSERT INTO Layout(Name) VALUES("スライドショー画像4");

INSERT INTO Numerical(Numerical, LayoutID, AccountID) VALUES('#F00', 1, 1), ('#FFF', 2, 1), ('#FFF', 3, 1), ('#F00', 4, 1), ('#000', 5, 1), ('#000', 6, 1), ('#FFF', 7, 1), ('static/images/slide/slide01.jpg', 8, 1), ('static/images/slide/slide05.jpg', 9, 1), ('static/images/slide/slide08.jpg', 10, 1), ('static/images/slide/slide10.jpg', 11, 1);
INSERT INTO Numerical(Numerical, LayoutID, AccountID) VALUES('#F00', 1, 2), ('#FFF', 2, 2), ('#FFF', 3, 2), ('#F00', 4, 2), ('#000', 5, 2), ('#000', 6, 2), ('#FFF', 7, 2), ('static/images/slide/slide01.jpg', 8, 2), ('static/images/slide/slide05.jpg', 9, 2), ('static/images/slide/slide08.jpg', 10, 2), ('static/images/slide/slide10.jpg', 11, 2);
INSERT INTO Numerical(Numerical, LayoutID, AccountID) VALUES('#F00', 1, 3), ('#FFF', 2, 3), ('#FFF', 3, 3), ('#F00', 4, 3), ('#000', 5, 3), ('#000', 6, 3), ('#FFF', 7, 3), ('static/images/slide/slide01.jpg', 8, 3), ('static/images/slide/slide05.jpg', 9, 3), ('static/images/slide/slide08.jpg', 10, 3), ('static/images/slide/slide10.jpg', 11, 3);
