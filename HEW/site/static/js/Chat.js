$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="ChatID" id="" class="size-input-ChatID"></td><td><input type="text" name="AccountID" id="" class="size-input-AccountID"></td><td><input type="text" name="SellID" id="" class="size-input-SellID"></td><td><input type="text" name="Content" id="" class="size-input-Content"></td><td><input type="text" name="Datetime" id="" class="size-input-Datetime"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});