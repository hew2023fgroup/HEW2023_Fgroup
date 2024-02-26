// class名を指定して要素を取得
var priceElements = document.getElementsByClassName("price");
var priceElements = document.getElementsByClassName("list-price");

// 三桁ごとにカンマを挿入する関数
function addCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// 全ての要素に対して処理を行う
for (var i = 0; i < priceElements.length; i++) {
    var price = priceElements[i].textContent;
    priceElements[i].textContent = addCommas(price);
}