$(function(){
    // #で始まるアンカーをクリックした場合に処理
    $('#box a[href^="#"]').click(function(){
    // $('#third_nav ul li a').click(function(){
      // 移動先を50px上にずらす
      var adjust = 150;
      // スクロールの速度
      var speed = 650; // ミリ秒
      // アンカーの値取得
      var href= $(this).attr("href");
      // 移動先を取得
      var target = $(href == "#" || href == "" ? 'html' : href);
      // 移動先を調整
      var position = target.offset().top - adjust;
      // スムーススクロール
      $('body,html').animate({scrollTop:position}, speed, 'swing');
      return false;
    });
  });
  
  
  $(function(){
    // #で始まるアンカーをクリックした場合に処理
    $('.guide-box a[href^="#"]').click(function(){
    // $('#third_nav ul li a').click(function(){
      // 移動先を50px上にずらす
      var adjust = 150;
      // スクロールの速度
      var speed = 650; // ミリ秒
      // アンカーの値取得
      var href= $(this).attr("href");
      // 移動先を取得
      var target = $(href == "#" || href == "" ? 'html' : href);
      // 移動先を調整
      var position = target.offset().top - adjust;
      // スムーススクロール
      $('body,html').animate({scrollTop:position}, speed, 'swing');
      return false;
    });
  });