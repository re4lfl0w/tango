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

    $('#likes').click(function () {
        var catid;
        catid = $(this).attr('data-catid');
        $.get('/rango/like_category/', {category_id: catid}, function (data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

    $('#suggestion').keyup(function () {
        var query;
        query = $(this).val();
        $.get('/rango/suggest_category/', {suggestion: query}, function (data) {
            $('#cats').html(data);
        });
    });

    $('.rango-add').click(function () {
        var catid;
        var title;
        var url;
        catid = $(this).attr('data-catid');
        title = $(this).attr('data-title');
        url = $(this).attr('data-url');
        $.get('/rango/auto_add_page/', {category_id: catid, title: title, url: url}, function (data) {
            $('#page').html(data);
        })
    })
});