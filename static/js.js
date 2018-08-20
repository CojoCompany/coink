function update_coin() {
    $.ajax({
        url: "/result"
    }).then(function(data) {
        $('#coin').attr('src', '/static/' + data.coin + 'euro.svg');
        $('#curve').attr('src', '/curve' + '?' + data.datetime);
    });
}


window.onload = function() {
    setInterval(update_coin, 100);
}
