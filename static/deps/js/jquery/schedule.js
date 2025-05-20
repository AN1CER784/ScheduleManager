$(document).ready(function () {
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('[id^="status-range"]').forEach(range => {
            const suffix = range.id.replace('status-range', '');
            const bar = document.getElementById('progress-bar' + suffix);
            if (bar) {
                const value = range.value;
                bar.style.width = value + '%';
                bar.textContent = value + '%';
            }
        });
    });

    document.addEventListener('input', function (event) {
        if (event.target.matches('[id^="status-range"]')) {
            const range = event.target;
            const suffix = range.id.replace('status-range', '');
            const bar = document.getElementById('progress-bar' + suffix);
            const value = range.value;

            if (bar) {
                bar.style.width = value + '%';
                bar.textContent = value + '%';
            }

            if (parseInt(value) === 100) {
                const accordionItem = range.closest('.accordion-item');
                const form = accordionItem?.querySelector('.complete-task-form');
                if (form) {
                    $(form).trigger('submit');
                }
            }

            $.ajax({
                type: 'POST',
                url: '/schedule/task-update-progress/',
                data: {
                    task_id: suffix,
                    complete_percentage: parseInt(value),
                    csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
            });
        }
    });

    const pendingTabBtn = document.querySelector('#pending-tab');
    bootstrap.Tab.getOrCreateInstance(pendingTabBtn).show();
    toggleNoTasksPlaceholder();
    toggleNoCompletedTasksPlaceholder();


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
    $(document).on('submit', '.complete-task-form', function completeTask(e) {
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
    $(document).on('submit', '.send-comment-form', function (e) {
        e.preventDefault();
        const form = $(this);
        const $container = form.closest('[id^="comment"]');
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

                const container = form.closest('[id^="comment"]');
                const commentList = container.find('.commentList');
                const dateId = response.comment_date;
                const dividerId = '#divider' + dateId;
                if (commentList.find(dividerId).length === 0) {
                    commentList.append(response.divider_html);
                }

                commentList.append(response.item_html)

                showMessage(response.message, true);
                toggleNoComments($container);
            },
            error: function () {
                showMessage('Server error. Try completing task.', false);
            }
        });
    });
    $(document).on('submit', '.incomplete-task-form', function (e) {
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
                $('#accordionPending').prepend($newItem);

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

    $(document).on('click', '.edit-btn', function () {
        const item = $(this).closest('.comment-item');
        item.find('.comment-view').addClass('d-none');
        item.find('.comment-edit-form').removeClass('d-none');
    });

    $(document).on('click', '.cancel-edit-btn', function () {
        const item = $(this).closest('.comment-item');
        item.find('.comment-edit-form').addClass('d-none');
        item.find('.comment-view').removeClass('d-none');
    });


    $(document).on('submit', '.comment-edit-form', function (e) {
        e.preventDefault();
        const form = $(this);
        const item = form.closest('.comment-item');

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    const $newItem = $(response.item_html);
                    item.replaceWith($newItem);
                    form.addClass('d-none');
                    item.find('.comment-view').removeClass('d-none');
                    showMessage(response.message, true);
                } else {
                    form.find('.form_errors').html(response.errors_html);
                    showMessage(response.message, false);
                }
            },
            error: function () {
                form.find('.form_errors').text('Server error, try again.');
            }
        });
    });
    $(document).on('submit', '.delete-comment-form', function (e) {
        e.preventDefault();
        const form = $(this);
        const $container = form.closest('[id^="comment"]');
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    form.closest('.comment-item').remove();
                    toggleNoComments($container);
                    showMessage(response.message, true);

                } else {
                    showMessage('Could not delete task.', false);
                }
            },
            error: function () {
                showMessage('Server error. Try deleting task.', false);
            }
        });
    });

    function toggleNoComments($container) {
        const $commentList = $container.find('.commentList');
        const hasComments = $commentList.find('.comment-item').length > 0;
        console.log(hasComments);
        if (!hasComments) {
            $commentList.empty();
        }
    }

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
});