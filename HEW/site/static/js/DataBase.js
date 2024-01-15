/*---------------Account---------------*/
$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="AccountID" id="AccountID" class="size-input-AccountID"></td><td><input type="text" name="UserName" id="UserName" class="size-input-UserName"></td><td><input type="text" name="Password" id="Password" class="size-input-Pass"></td><td><input type="text" name="Birthday" id="Birthday" class="size-input-Birth" maxlength="8"></td><td><input type="text" name="SexID" id="SexID" class="size-input-SexID"></td><td><input type="text" name="MailAddress" id="MailAddress" class="size-input-Mail"></td><td><input type="text" name="KanjiName" id="KanjiName" class="size-input-KanjiName"></td><td><input type="text" name="Furigana" id="Furigana" class="size-input-Furigana"></td><td><input type="text" name="RegistDate" id="RegistDate" class="size-input-Regist"></td><td><input type="text" name="Money" id="Money"  class="size-input-Money"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});



/*---------------Address---------------*/
$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="AddressID" id="AddressID" class="size-input-AddressID"></td><td><input type="text" name="Address" id="Address" class="size-input-Address"></td><td><input type="text" name="POST" id="POST" class="size-input-POST" maxlength="8"></td><td><input type="text" name="AccountID" id="AccountID" class="size-input-AccountID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});