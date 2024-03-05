// 出品ページのタグINPUTするタグを追加しています

var container = document.getElementById("container");
var counter = container.querySelectorAll('input[type="text"][name^="tag"]').length;

function addInput() {
    if (counter >= 20) return;
    
    // 新しいinput要素を作成
    var input = document.createElement("input");
    input.type = "text";
    input.value = "#";
    input.style = "margin:3px";
    input.name = "tag" + counter;

    // 削除ボタン
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "-";
    deleteButton.type = "button";
    deleteButton.onclick = function() {
        container.removeChild(input);
        container.removeChild(deleteButton);
    };

    container.appendChild(input);
    container.appendChild(deleteButton);
    
    counter++;
}
