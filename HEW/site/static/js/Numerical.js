$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="NumericalID" id="" class="size-input-NumericalID"></td><td><input type="text" name="Numerical" id="" class="size-input-Numerical"></td><td><input type="text" name="LayoutID" id="" class="size-input-LayoutID"></td><td><input type="text" name="AccountID" id="" class="size-input-AccountID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});