function price_update(){
    var dio = document.getElementById('dio').value;
    var price_to_populate = document.getElementsByName(dio)[0].cells[0].innerText;
    document.getElementsByName('current_price')[0].innerText = price_to_populate
}