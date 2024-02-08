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