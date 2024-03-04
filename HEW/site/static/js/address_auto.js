$(function() {
    $('#post').on('keyup', function() {
        let postalCode = $(this).val().replace('-', ''); // ハイフンを除去する
        if (postalCode.length === 7) {
            $.getJSON('https://zipcloud.ibsnet.co.jp/api/search?zipcode=' + postalCode, function(data) {
                if (data.status === 200) {
                    $('#address').val(data.results[0].address1 + data.results[0].address2 + data.results[0].address3);
                } else {
                    $('#address').val('');
                }
            });
        } else {
            $('#address').val('');
        }
    });
});