$(function() {
    $('#submit').attr('disabled', 'disabled'); //①
        $('#chkbox').click(function() { //②
        if ( $(this).prop('checked') == false ) {　//③
            $('#submit').attr('disabled', 'disabled');　//④
        } else {
            $('#submit').removeAttr('disabled');　//⑤
        }
    });
});