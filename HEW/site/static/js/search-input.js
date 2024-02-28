document.getElementById('searchInput').addEventListener('click', function() {
    var searchHistory = document.querySelector('.search-history');
    if (searchHistory && searchHistory.children.length > 0) {
        if (searchHistory.style.display === 'none') {
            searchHistory.style.display = 'block';
        } else {
            searchHistory.style.display = 'none';
        }
    }
});

document.getElementById('closebtn').addEventListener('click', function() {
    var searchHistory = document.querySelector('.search-history');
    if (searchHistory) {
        searchHistory.style.display = 'none';
    }
});

document.getElementById("searchInput").addEventListener("keydown", function(event) {
    var searchHistory = document.querySelector('.search-history');
    if (searchHistory) {
        searchHistory.style.display = 'none';
    }
});








// JavaScript
// 検索履歴のボタン要素のリストを取得
var searchButtons = document.querySelectorAll('.search-history li button');

// 下線を引く回数の上限
var maxUnderlines = 3;

// ページが読み込まれたときに下線を制御する関数
function controlUnderlines() {
    // 下線を引く回数の上限に達したら、それ以上のボタンには下線を描画しない
    for (var i = 0; i < searchButtons.length; i++) {
        if (i >= maxUnderlines) {
            searchButtons[i].classList.add('no-underline');
        } else {
            searchButtons[i].classList.remove('no-underline');
        }
    }
}

// ページ読み込み時に下線を制御
controlUnderlines();

