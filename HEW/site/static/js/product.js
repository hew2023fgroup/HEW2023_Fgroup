$(function() {  
  $slide = $('.slide');
  $navigation = $('.slide-navigation .item');
 
  $slide.slick({  //slickスライダー作成
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
  });  
  $navigation.each(function(index){ //サムネイルに連番付与属性
    $(this).attr('data-number', index);
  });
  $navigation.eq(0).addClass('current');  //1枚をオーバーレイ
  
  $navigation.on('click', function(){ //サムネイルクリック時イベント
    var number = $(this).attr('data-number');
    $slide.slick('slickGoTo', number, true);
    $(this).siblings().removeClass('current');
    $(this).addClass('current');
  });
});



// gift 数量
$(function() {
  $('.spinner').each(function() {
    var el  = $(this);
    var add = $('.spinner-add');
    var sub = $('.spinner-sub');

    // substract
    el.parent().on('click', '.spinner-sub', function() {
      if (el.val() > parseInt(el.attr('min'))) {
        el.val(function(i, oldval) {
          return --oldval;
        });
      }
      // disabled
      if (el.val() == parseInt(el.attr('min'))) {
        el.prev(sub).addClass('disabled');
      }
      if (el.val() < parseInt(el.attr('max'))) {
        el.next(add).removeClass('disabled');
      }
    });

    // increment
    el.parent().on('click', '.spinner-add', function() {
      if (el.val() < parseInt(el.attr('max'))) {
        el.val(function(i, oldval) {
          return ++oldval;
        });
      }
      // disabled
      if (el.val() > parseInt(el.attr('min'))) {
        el.prev(sub).removeClass('disabled');
      }
      if (el.val() == parseInt(el.attr('max'))) {
        el.next(add).addClass('disabled');
      }
    });
  });
});

const bookmark = document.getElementById("bookmark");
// flagがtrueのときはデータを取得、falseのときはデータを削除
var flag = false;
function colorChange(){
    // classListでクラスを取得(今回はaquaクラスを取得)
    // toggleでクラスを付け外しする
    bookmark.classList.toggle("aqua");
    // flagを反転
    flag = !flag;
    console.log(flag);
}
bookmark.addEventListener("click", colorChange);