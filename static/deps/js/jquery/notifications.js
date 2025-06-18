function showMessage(message, success = true) {
    let alertType = success ? 'bg-success text-white ' : 'bg-white text-danger'
    let html = `<div id="notification" class="position-fixed start-50 translate-middle-x z-3 alert fade show shadow-sm ${alertType} border border-dark" role="alert">
                  ${message}
                </div>`;
    $('#message-container').html(html);
    setTimeout(function () {
        $('#message-container').html('');
    }, 3000);
}

$(document).ready(function () {
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 3000);
    }
    var notification_warning = $('#notification-warning');
    if (notification_warning.length > 0) {
        setTimeout(function () {
            notification_warning.alert('close');
        }, 3000);
    }


});