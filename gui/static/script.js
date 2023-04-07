function updateString() {
    $.get('/get_string', function(data) {
        $('#string').val(data);
    });
}

setInterval(updateString, 1000);