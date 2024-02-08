document.getElementById("imagePreview").addEventListener("click", function(event) {
    if (event.target.tagName !== "INPUT") {
        event.preventDefault();
        var images = document.getElementsByClassName("preview-image");
        for (var i = 0; i < images.length; i++) {
            images[i].removeAttribute("id");
            images[i].style.backgroundColor = ""; // 背景色をクリア
        }
        if (event.target.classList.contains("preview-image")) {
            event.target.id = "thumbnail";
            event.target.style.backgroundColor = "blue"; // 背景色を青色に変更

            // クリックされた画像を別の場所に表示
            var thumbnailContainer = document.getElementById("thumbnailContainer");
            thumbnailContainer.innerHTML = ''; // 切り替える前に中身をクリア
            var imageCopy = event.target.cloneNode(true); // クリックされた画像のコピーを作成
            thumbnailContainer.appendChild(imageCopy);
        }
    }
});


function updateThumbnail(src) {
        var thumbnailContainer = document.getElementById("thumbnailContainer");
        thumbnailContainer.innerHTML = ""; // サムネイルコンテナをクリア
        var thumbnailImage = new Image();
        thumbnailImage.src = src;
        thumbnailContainer.appendChild(thumbnailImage);
    }



function previewImages(event) {
    event.preventDefault();

    var files = event.target.files || event.dataTransfer.files; // どちらの方法でもファイルを取得できるようにする
    var preview = document.getElementById("previewContainer");

    // 配列をループするための再帰関数を定義
    function readFile(index) {
        if (index >= files.length) return; // ベースケース: 全てのファイルを処理したら終了

        var reader = new FileReader();
        reader.onload = function(e) {
            var container = document.createElement("div");
            container.className = "preview-image-container";

            var image = new Image();
            image.src = e.target.result;
            image.className = "preview-image";

            var deleteButton = document.createElement("button");
            deleteButton.className = "delete-button";
            deleteButton.innerHTML = "<img src='static/images/x-white.svg' alt='削除'>";

            deleteButton.onclick = function() {
                // 画像を削除する際にIDも削除
                if (image.id === "thumbnail") {
                    image.removeAttribute("id");
                    // サムネイルを削除
                    var thumbnailContainer = document.getElementById("thumbnailContainer");
                    thumbnailContainer.innerHTML = '';
                }
                container.remove();
            };

            container.appendChild(image);
            container.appendChild(deleteButton);

            preview.appendChild(container);

            // 画像読み込み後にクリックイベントを設定
            image.onload = function() {
                image.addEventListener("click", function(event) {
                    event.preventDefault();
                    var images = document.getElementsByClassName("preview-image");
                    for (var i = 0; i < images.length; i++) {
                        images[i].removeAttribute("id");
                        images[i].style.backgroundColor = ""; // 背景色をクリア
                        images[i].style.border = ""; // 線をクリア
                    }
                    if (image.classList.contains("preview-image")) {
                        image.id = "thumbnail";
                        image.style.border = "2px solid red"; 

                        // image.style.backgroundColor = "blue"; // 背景色を青色に変更
                        updateThumbnail(image.src); // サムネイル更新
                    }
                });
            };

            // 次のファイルを処理するために再帰呼び出し
            readFile(index + 1);
        };
        reader.readAsDataURL(files[index]);
    }

    // 再帰呼び出しを開始
    readFile(0);
}




