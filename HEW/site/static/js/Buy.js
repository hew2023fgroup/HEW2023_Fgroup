$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="BuyID" id="" class="size-input-BuyID"></td><td><input type="text" name="SellID" id="" class="size-input-SellID"></td><td><input type="text" name="AccountID" id="" class="size-input-AccountID"></td><td><input type="text" name="Review" id="" class="size-input-Review"></td><td><input type="text" name="Datetime" id="" class="size-input-Datetime"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});