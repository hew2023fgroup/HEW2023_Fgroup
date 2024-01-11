$(function () {

    // フォームの入力値
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    document.getElementById('disp_username').innerHTML = username;
    document.getElementById('disp_email').innerHTML = email;
    document.getElementById('disp_password').innerHTML = passwword;

    $('#openModal').click(function(){
        $('#modalArea').fadeIn();
    });
    $('#closeModal , #modalBg').click(function(){
      $('#modalArea').fadeOut();
    });
  });