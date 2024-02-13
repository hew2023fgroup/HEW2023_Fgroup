function updateThumbnail(src) {
    var thumbnailContainer = document.getElementById("thumbnailContainer");
    if (thumbnailContainer) {
        thumbnailContainer.innerHTML = ""; // サムネイルコンテナをクリア
        var thumbnailImage = new Image();
        thumbnailImage.src = src;
        thumbnailContainer.appendChild(thumbnailImage);
    } else {
        console.error("エラー: #thumbnailContainer 要素が見つかりません。");
    }
}

document.getElementById("imagePreview").addEventListener("click", function(event) {
    // クリックされた要素が <input> でない場合の処理
    if (event.target.tagName !== "INPUT") {
        event.preventDefault(); // イベントのデフォルト動作をキャンセル

        // すべてのプレビュー画像から ID を削除し、背景色をクリア
        var images = document.getElementsByClassName("preview-image");
        for (var i = 0; i < images.length; i++) {
            images[i].removeAttribute("id");
            images[i].style.backgroundColor = "";
        }

        // クリックされた要素がプレビュー画像である場合の処理
        if (event.target.classList.contains("preview-image")) {
            // クリックされた画像に ID を設定し、背景色を青に変更
            event.target.id = "thumbnail";
            // event.target.style.backgroundColor = "blue";

            // クリックされた画像を別の場所に表示
            var thumbnailContainer = document.getElementById("thumbnailContainer");
            if (thumbnailContainer) {
                thumbnailContainer.innerHTML = ''; // 切り替える前に中身をクリア
                var imageCopy = event.target.cloneNode(true); // クリックされた画像のコピーを作成
                thumbnailContainer.appendChild(imageCopy);
            } else {
                console.error("エラー: #thumbnailContainer 要素が見つかりません。");
            }
        }
    }
});

function previewImages(event) {
    event.preventDefault();

    var files = event.target.files || event.dataTransfer.files;
    var preview = document.getElementById("previewContainer");

    function readFile(index) {
        if (index >= files.length) return;

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
                if (image.id === "thumbnail") {
                    image.removeAttribute("id");
                    var thumbnailContainer = document.getElementById("thumbnailContainer");
                    if (thumbnailContainer) {
                        thumbnailContainer.innerHTML = '';
                    } else {
                        console.error("エラー: #thumbnailContainer 要素が見つかりません。");
                    }
                }
                container.remove();
            };

            container.appendChild(image);
            container.appendChild(deleteButton);

            preview.appendChild(container);

            image.onload = function() {
                image.addEventListener("click", function(event) {
                    event.preventDefault();
                    var images = document.getElementsByClassName("preview-image");
                    for (var i = 0; i < images.length; i++) {
                        images[i].removeAttribute("id");
                        images[i].style.backgroundColor = "";
                        images[i].style.border = "";
                    }
                    if (image.classList.contains("preview-image")) {
                        image.id = "thumbnail";
                        // image.style.backgroundColor = "blue";
                        image.style.border = "3px solid #fc94af";


                        updateThumbnail(image.src);
                        document.getElementById("select").value = files[index].name; // ここでファイル名を #select の value にセット
                        console.log("ファイル名が #select の value に格納されました: " + files[index].name); // コンソールログを出力
                    }
                });
            };

            readFile(index + 1);
        };
        reader.readAsDataURL(files[index]);
    }

    readFile(0);
}
