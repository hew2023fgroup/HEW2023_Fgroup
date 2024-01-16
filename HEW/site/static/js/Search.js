$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="SearchID" id="" class="size-input-SearchID"></td><td><input type="text" name="Word" id="" class="size-input-Word"></td><td><input type="text" name="AccountID" id="" class="size-input-AccountID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});