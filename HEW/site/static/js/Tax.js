$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="TaxID" id="" class="size-input-TaxID"></td><td><input type="text" name="Section" id="" class="size-input-Section" maxlength="2"></td><td><input type="text" name="Tax" id="" class="size-input-Tax"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});