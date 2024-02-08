document.addEventListener('DOMContentLoaded', function () {
    var button = document.getElementById('hoverButton');
    var hiddenArea = document.getElementById('hiddenArea');
    var isHovered = false;
    var timeout;

    function showHiddenArea() {
      clearTimeout(timeout);
      isHovered = true;
      hiddenArea.style.display = 'block';
      requestAnimationFrame(function () {
        hiddenArea.style.opacity = '1';
        hiddenArea.style.transform = 'translateY(0) translateX(12%)'; /* 上から滑らかに現れる */
        // button.style.textDecoration = 'underline';
      }, 400); /* 表示するスピード */
    }

    function hideHiddenArea() {
      if (isHovered) {
        timeout = setTimeout(function () {
          isHovered = false;
          hiddenArea.style.opacity = '0';
          hiddenArea.style.transform = 'translateY(-100%) translateX(12%)'; /* 上に隠れる */
          setTimeout(function () {
            if (!isHovered) {
              hiddenArea.style.display = 'none';
              // button.style.textDecoration = 'none';
            }
          }, 1000); /* transitionが終わったら非表示にする */
        }, 750);
      }
    }

    button.addEventListener('mouseenter', showHiddenArea);

    button.addEventListener('mouseleave', hideHiddenArea);

    hiddenArea.addEventListener('mouseenter', function () {
      clearTimeout(timeout);
    });

    hiddenArea.addEventListener('mouseleave', hideHiddenArea);
  });


