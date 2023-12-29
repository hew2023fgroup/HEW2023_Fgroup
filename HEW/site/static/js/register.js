function confirmRegistration() {
    // フォームの入力値
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // 確認メッセージ
    var confirmationMessage = 'ユーザーネーム: ' + username + '\nメールアドレス: ' + email + '\nパスワード: ' + password + '\n\nこの情報で登録してもよろしいですか？';

    // 表示
    var confirmed = confirm(confirmationMessage);

    // 確認ボタン
    if (confirmed) {
        // フォームをサブミット
        document.forms['RegistrationForm'].action = "/register/";
    } else {
        // 確認がキャンセルされた場合、通常のフォームサブミットを阻止
        event.preventDefault();
    }
}