function onInventoryQuickUpdate(id) {
    var amount = $('#amount_' + id).val();
    $('#update_' + id).attr('href', "/inventory/quick_edit/" + id + "/" + amount + "/");
}