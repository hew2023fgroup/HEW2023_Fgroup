/*---------------SellIMG---------------*/
$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="SellIMGID" id="" class="size-input-SellIMGID"></td><td><input type="text" name="SellIMG" id="" class="size-input-SellIMG"></td><td><input type="text" name="ThumbnailFlg" id="" class="size-input-ThumbnailFlg"></td><td><input type="text" name="SellID" id="" class="size-input-SellID"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});