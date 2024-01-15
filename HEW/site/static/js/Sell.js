/*---------------Sell---------------*/
$(function(){
    $('tbody').sortable();

    $('#addRow').click(function(){
        var html = '<tr><td><input type="text" name="SellID" id="SellID" class="size-input-SellID"></td><td><input type="text" name="Name" id="Name" class="size-input-Name"></td><td><input type="text" name="Price" id="Price" class="size-input-Price"></td><td><input type="text" name="TaxID" id="TaxID" class="size-input-TaxID"></td><td><input type="text" name="PostageID" id="PostageID" class="size-input-PostageID"></td><td><input type="text" name="StatusID" id="StatusID" class="size-input-StatusID"></td><td><input type="text" name="Overview" id="Overview" class="size-input-Overview"></td><td><input type="text" name="ScategoryID" id="ScategoryID" class="size-input-ScategoryID"></td><td><input type="text" name="AccountID" id="AccountID" class="size-input-AccountID"></td><td><input type="text" name="Datetime" id="Datetime" class="size-input-Datetime"></td><td><input type="text" name="draft" id="draft" class="size-input-draft"></td><td><button class="remove">-</button></td></tr>';
        $('tbody').append(html);
    });

    $(document).on('click', '.remove', function() {
        $(this).parents('tr').remove();
    });
});