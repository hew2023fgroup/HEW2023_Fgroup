$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="TagID" id="" class="size-input-TagID"></td><td><input type="text" name="Name" id="" class="size-input-Name"></td><td><input type="text" name="SellID" id="" class="size-input-SellID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});