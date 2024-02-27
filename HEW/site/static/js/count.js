// class名を指定して要素を取得
var priceElements = document.getElementsByClassName("price");
var listPriceElements = document.getElementsByClassName("list-price");
var productDetailPriceElements = document.getElementsByClassName("product-detail-price");

// 三桁ごとにカンマを挿入する関数
function addCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// "price" クラスの要素に対して処理を行う
for (var i = 0; i < priceElements.length; i++) {
    var price = parseInt(priceElements[i].textContent); // 文字列を整数に変換
    priceElements[i].textContent = addCommas(price);
}

// "list-price" クラスの要素に対して処理を行う
for (var i = 0; i < listPriceElements.length; i++) {
    var listPrice = parseInt(listPriceElements[i].textContent); // 文字列を整数に変換
    listPriceElements[i].textContent = addCommas(listPrice);
}

// "product-detail-price" クラスの要素に対して処理を行う
for (var i = 0; i < productDetailPriceElements.length; i++) {
    var productDetailPrice = parseInt(productDetailPriceElements[i].textContent); // 文字列を整数に変換
    productDetailPriceElements[i].textContent = addCommas(productDetailPrice);
}
