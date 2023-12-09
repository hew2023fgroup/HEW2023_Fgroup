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
  `Money` int
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
INSERT INTO Scategory(Name,McategoryID) VALUES("靴",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("靴",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("バッグ",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("バッグ",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("アクセサリー",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("アクセサリー",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("ファッション小物",1);
INSERT INTO Scategory(Name,McategoryID) VALUES("ファッション小物",2);
INSERT INTO Scategory(Name,McategoryID) VALUES("ベビー服",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("キッズ服",3);
INSERT INTO Scategory(Name,McategoryID) VALUES("キッズ靴",3);
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

INSERT INTO Address(Address,POST,AccountID) VALUES("愛知県名古屋市中村区名駅4-27-1HAL名古屋","450-0002",1);

INSERT INTO Sell(Name,Price,TaxID,PostageID,StatusID,Overview,ScategoryID,AccountID,draft) VALUES("Sample商品データ",2000,1,2,2,"サンプルデータです。最終的には削除するデータです。",6,1,0);

INSERT INTO SellIMG(SellIMG,SellID) VALUES("static/images/sell/Product (1).jpeg",1);
