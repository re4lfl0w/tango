$(document).ready(function () {
    $('#about-btn').click(function (event) {
        msgstr = $('#msg').html()
        msgstr += 'o'
        $('#msg').html(msgstr)
    });

    $('p').hover(
        function () {
            $(this).css('color', 'red');
        },
        function () {
            $(this).css('color', 'black');
        }
    );

    $('#about-btn').addClass('btn btn-primary')
});