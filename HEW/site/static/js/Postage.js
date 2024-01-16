$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="PostageID" id="" class="size-input-PostageID"></td><td><input type="text" name="Size" id="" class="size-input-Size" maxlength="2"></td><td><input type="text" name="Price" id="" class="size-input-Price"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});