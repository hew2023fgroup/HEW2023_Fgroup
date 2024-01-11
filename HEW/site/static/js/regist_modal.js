$(function () {
  $('#openModal').click(function(){
      // フォーム内の表示内容をモーダルウィンドウ内にコピー
      $('#modal_disp_usename').text($('#disp_usename').text());
      $('#modal_disp_email').text($('#disp_email').text());
      $('#modal_disp_password').text($('#disp_password').text());

      $('#modalArea').fadeIn();
  });

  $('#btn').click(function(event){
      event.preventDefault(); // デフォルトのサブミット動作をキャンセル

      // 他のサブミットボタンの処理...

      // モーダルウィンドウを閉じる
      $('#modalArea').fadeOut();
  });
  
  $('#closeModal , #modalBg').click(function(){
      $('#modalArea').fadeOut();
  });
});