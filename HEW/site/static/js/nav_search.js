// navbtnをクリックしたときの処理
document.getElementById("navbtn").onclick = function(){
    // html要素にopenクラスを追加
    document.querySelector('html').classList.add('open');
  
  // closebtnを表示
    document.getElementById("closebtn").style.display = 'block';
    document.getElementById("closebtn").style.transition = 'opacity 3.3s';
    document.getElementById("closebtn").style.opacity = '1';
}
  
// closebtnをクリックしたときの処理
document.getElementById("closebtn").onclick = function(){
    // html要素からopenクラスを削除
    document.querySelector('html').classList.remove('open');
  
    document.getElementById("closebtn").style.display = 'none';
  
    // ×を押したら検索フォームのinputの中身を空にする
    document.getElementById('searchInput').value = '';
}
  
  // 検索フォームでEnterキーが押されたときの処理
document.getElementById("searchInput").addEventListener("keydown", function(event) {
    // キーがEnter（キーコード13）の場合
    if (event.keyCode === 13) {
      // openクラスを削除
      document.querySelector('html').classList.remove('open');
  
      document.getElementById('searchInput').value = '';
    }
});