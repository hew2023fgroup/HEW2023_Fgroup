// navbtnをクリックしたときの処理
document.getElementById("hoverButton").onclick = function(){
    // html要素にopenクラスを追加
    document.querySelector('html').classList.add('open_cate');
  
  // closebtnを表示
    document.getElementById("cate_closebtn").style.display = 'block';
    document.getElementById("cate_closebtn").style.transition = 'opacity 3.3s';
    document.getElementById("cate_closebtn").style.opacity = '1';
}
  
// closebtnをクリックしたときの処理
document.getElementById("cate_closebtn").onclick = function(){
    // html要素からopenクラスを削除
    document.querySelector('html').classList.remove('open_cate');
  
    document.getElementById("cate_closebtn").style.display = 'none';
  
    // ×を押したら検索フォームのinputの中身を空にする
    document.getElementById('searchInput').value = '';
}
  
  // 検索フォームでEnterキーが押されたときの処理
document.getElementById("searchInput").addEventListener("keydown", function(event) {
    // キーがEnter（キーコード13）の場合
    if (event.keyCode === 13) {
      // openクラスを削除
      document.querySelector('html').classList.remove('open_cate');
  
      document.getElementById('searchInput').value = '';
    }
});