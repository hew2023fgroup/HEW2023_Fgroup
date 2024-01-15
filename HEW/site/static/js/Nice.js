$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="NiceID" id="" class="size-input-NiceID"></td><td><input type="text" name="AccountID" id="" class="size-input-AccountID"></td><td><input type="text" name="SellID" id="" class="size-input-SellID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});