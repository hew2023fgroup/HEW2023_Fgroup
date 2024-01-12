$(function(){
    // 条件に基づいてJavaScriptの処理を行う
    $('#modal_disp_usename').text($('#disp_usename').text());
    $('#modal_disp_email').text($('#disp_email').text());
    $('#modal_disp_password').text($('#disp_password').text());

    $('#modalArea').fadeIn();
});

$('#btn').click(function(){
    // モーダルウィンドウを閉じる
    $('#modalArea').fadeOut();
});

$('#closeModal , #modalBg').click(function(){
    $('#modalArea').fadeOut();
});