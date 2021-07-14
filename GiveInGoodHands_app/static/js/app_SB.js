function show_id(event)
{
    var ids = get_checked_chexboxes();
    var params = new URLSearchParams();
    ids.forEach(id => params.append("type_ids", id))
    var address = '/get_institutions_by_category?'+ params.toString();
    fetch(address)
        .then(response => response.text())
        .then(data => document.getElementById("institutions").innerHTML = data);

}
function get_checked_chexboxes()
{
    var markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
    // :checked - zaznaczone checboxy
    var ids = [];
    markedCheckbox.forEach(box => ids.push(box.value));
    console.log(ids);
    return ids;
}



$( document ).ready(function() {
    var li_buttons = $('.checkboxy');//document.getElementsByClassName('checkboxy');
    li_buttons.click(show_id);
});