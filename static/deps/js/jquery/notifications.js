
function showMessage(message, success = true) {
    const stack = $('#notification-stack');
    const type = success ? 'success' : 'warning';
    const notice = $(
        `<div class="notice notice-${type}">
            <div class="notice-bar"></div>
            <div class="notice-message">${message}</div>
            <button type="button" class="notice-close" aria-label="Close">?</button>
        </div>`
    );
    stack.append(notice);
    setTimeout(function () {
        notice.fadeOut(200, function () { $(this).remove(); });
    }, 3500);
}

$(document).ready(function () {
    $(document).on('click', '.notice-close', function () {
        $(this).closest('.notice').remove();
    });
    setTimeout(function () {
        $('#notification-stack .notice').each(function () {
            $(this).fadeOut(200, function () { $(this).remove(); });
        });
    }, 3500);
});
