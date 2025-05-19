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