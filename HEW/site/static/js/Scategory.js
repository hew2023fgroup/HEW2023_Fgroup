$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="ScategoryID" id="" class="size-input-ScategoryID"></td><td><input type="text" name="Name" id="" class="size-input-Name"></td><td><input type="text" name="McategoryID" id="" class="size-input-McategoryID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});