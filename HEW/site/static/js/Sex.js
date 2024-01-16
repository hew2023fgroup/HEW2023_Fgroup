/*---------------Sex---------------*/
$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="SexID" id="SexID" class="size-input-SexID"></td><td><input type="text" name="Sex" id="Sex" class="size-input-Sex"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});