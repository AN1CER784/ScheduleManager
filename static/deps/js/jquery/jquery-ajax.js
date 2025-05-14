$(document).ready(function () {
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 3000);
    }
    const pendingTabBtn = document.querySelector('#pending-tab');
    bootstrap.Tab.getOrCreateInstance(pendingTabBtn).show();
    toggleNoTasksPlaceholder();
    toggleNoCompletedTasksPlaceholder();


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


    // Добавление задачи
    $('#task-add-form').on('submit', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (!response.success) {
                    const errorsHtml = response.errors_html

                    form.find('.form_errors').html(errorsHtml);
                    return showMessage(response.message, false);
                }

                form.find('.form_errors').empty();


                const $newItem = $(response.html.trim());

                let containerSelector;
                if (response.type === 'pending') {
                    containerSelector = '#accordionPending';
                } else if (response.type === 'done') {
                    containerSelector = '#accordionDone';
                } else {
                    containerSelector = '#accordionPending';
                }

                $(containerSelector).prepend($newItem);

                $newItem.find('.accordion-collapse').addClass('show');

                form[0].reset();
                showMessage(response.message, true);
                toggleNoTasksPlaceholder();
                toggleNoCompletedTasksPlaceholder();
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });
    });
    $(document).on('submit', '.complete-task-form', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (!response.success) {
                    const errorsHtml = response.errors_html !== undefined
                        ? response.errors_html
                        : response.html || '';

                    form.find('.form_errors').html(errorsHtml);
                    return showMessage(response.message, false);
                }

                form.find('.form_errors').empty();

                const $newItem = $(response.html.trim());
                form.closest('.accordion-item').remove();
                $('#accordionDone').prepend($newItem);

                showMessage(response.message, true);
                toggleNoTasksPlaceholder();
                toggleNoCompletedTasksPlaceholder();
            },
            error: function () {
                showMessage('Server error. Try completing task.', false);
            }
        });
    });


    $(document).on('submit', '.delete-task-form', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    form.closest('.accordion-item').remove();
                    showMessage(response.message, true);
                    toggleNoTasksPlaceholder();
                    toggleNoCompletedTasksPlaceholder();
                } else {
                    showMessage('Could not delete task.', false);
                }
            },
            error: function () {
                showMessage('Server error. Try deleting task.', false);
            }
        });
    });

    function toggleNoTasksPlaceholder() {
        const $accordion = $('#accordionPending');
        const hasItems = $accordion.children('.accordion-item').length > 0;
        if (hasItems) {
            $('#no-tasks-placeholder').hide();
            $accordion.show();
        } else {
            $accordion.hide();
            $('#no-tasks-placeholder').show();
        }
    }

    function toggleNoCompletedTasksPlaceholder() {
        const $accordion = $('#accordionDone');
        const hasItems = $accordion.children('.accordion-item').length > 0;
        if (hasItems) {
            $('#no-completed-tasks-placeholder').hide();
            $accordion.show();
        } else {
            $accordion.hide();
            $('#no-completed-tasks-placeholder').show();
        }
    }
});