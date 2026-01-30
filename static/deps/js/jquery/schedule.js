$(document).ready(function () {
    $('.tab-btn').on('click', function () {
        const target = $(this).data('target');
        $('.tab-btn').removeClass('active');
        $(this).addClass('active');
        $('.tab-panel').removeClass('active');
        $(target).addClass('active');
    });
});
