$(document).ready(function () {

    toggleNoTasksPlaceholder();
    toggleNoCompletedTasksPlaceholder();


    $(document).on('click', '.accordion-toggle', function () {
        const target = $($(this).data('target'));
        const $this = $(this);
        if (target.length) {
            target.slideToggle(200, function () {
                updateProgressBars(target);
            });
            $this.toggleClass('open');
        }
    });

    function initTaskViewer() {
        const $taskList = $('#mainContent');
        const $taskDetails = $('#taskDetails');

        $(document).off('click.task-viewer').on('click.task-viewer', '.show-task-btn', function () {
            const $item = $(this).closest('.accordion-item');
            const $accordionCollapse = $item.children('.accordion-collapse');

            if ($accordionCollapse.length === 0) return;

            $taskDetails.removeClass('d-none').empty();
            $taskList.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
            $taskDetails.addClass('col-12 col-lg-6');

            const $clone = $accordionCollapse.clone().css('display', 'block');
            $taskDetails.append($clone);

            updateProgressBars($taskDetails);
        });

        updateProgressBars($(document));
    }

    function updateProgressBars($scope = $(document)) {
        $scope.find('[id^="status-range"]').each(function () {
            const $range = $(this);
            const suffix = this.id.replace('status-range', '');
            const $bar = $scope.find('#progress-bar' + suffix);

            if ($bar.length) {
                const value = $range.val();
                $bar.css('width', value + '%').text(value + '%');

                $range.off('input.progress').on('input.progress', function () {
                    const newVal = $(this).val();
                    $bar.css('width', newVal + '%').text(newVal + '%');
                });
            }
        });
    }

    initTaskViewer();

    $(document).on('click', '.close-task-btn', function () {
        const $taskDetails = $('#taskDetails');
        const $taskList = $('#mainContent');

        $taskDetails.addClass('d-none').empty();
        $taskList.removeClass('col-lg-5').addClass('col-lg-8 col-xxl-6');
        $taskDetails.removeClass('col-12 col-lg-6');
    });

    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    const sendProgressUpdate = debounce(function (taskId, value) {
        const projectId = $('#project-data').data('project-id');
        $.ajax({
            type: 'POST',
            url: `/users/projects/${projectId}/tasks/task-update-progress/`,
            data: {
                task_id: taskId,
                complete_percentage: value,
                csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
        });
    }, 500);

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
                const accordionId = range.closest('.accordion-collapse.collapse').id;
                const accordionItem = document.getElementById("task-" + accordionId)
                console.log(accordionItem);
                const form = accordionItem?.querySelector('.complete-task-form');
                if (form) {
                    $(form).trigger('submit');
                }
            }

            sendProgressUpdate(suffix, value);
        }
    });



    $('#task-add-form').on('submit', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (!response.success) {
                    const errorsHtml = response.item_html

                    form.find('.form_errors').html(errorsHtml);
                    return showMessage(response.message, false);
                }

                form.find('.form_errors').empty();


                const $newItem = $(response.item_html.trim());

                let containerSelector;
                if (response.type === 'InProgress') {
                    containerSelector = '#accordionInProgress';
                } else if (response.type === 'Done') {
                    containerSelector = '#accordionDone';
                } else {
                    containerSelector = '#accordionInProgress';
                }

                $(containerSelector).prepend($newItem);

                showMessage(response.message, true);
                toggleNoTasksPlaceholder();
                toggleNoCompletedTasksPlaceholder();
                initTaskViewer();
                form.trigger('reset');
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
                    const errorsHtml = response.item_html !== undefined
                        ? response.item_html
                        : response.item_html || '';

                    form.find('.form_errors').html(errorsHtml);
                    return showMessage(response.message, false);
                }

                form.find('.form_errors').empty();

                const $newItem = $(response.item_html.trim());

                const $oldAccordionItem = form.closest('.accordion-item');
                $oldAccordionItem.remove();

                $('#accordionDone').prepend($newItem);

                const $taskDetails = $('#taskDetails');
                const $taskList = $('#mainContent');
                $taskDetails.removeClass('d-none').empty();
                $taskList.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
                $taskDetails.addClass('col-12 col-lg-6');

                const $accordionCollapse = $newItem.find('.accordion-collapse').first();
                const $clone = $accordionCollapse.clone().css('display', 'block');
                $taskDetails.append($clone);

                showMessage(response.message, true);
                toggleNoTasksPlaceholder();
                toggleNoCompletedTasksPlaceholder();
                initTaskViewer();
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
                    const errorsHtml = response.item_html !== undefined
                        ? response.item_html
                        : response.item_html || '';

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
                form.trigger('reset');
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
                    const errorsHtml = response.item_html !== undefined
                        ? response.item_html
                        : response.item_html || '';

                    form.find('.form_errors').html(errorsHtml);
                    return showMessage(response.message, false);
                }

                form.find('.form_errors').empty();

                const $newItem = $(response.item_html.trim());

                const $oldAccordionItem = form.closest('.accordion-item');
                $oldAccordionItem.remove();

                $('#accordionInProgress').prepend($newItem);

                const $taskDetails = $('#taskDetails');
                const $taskList = $('#mainContent');
                $taskDetails.removeClass('d-none').empty();
                $taskList.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
                $taskDetails.addClass('col-12 col-lg-6');

                const $accordionCollapse = $newItem.find('.accordion-collapse').first();
                const $clone = $accordionCollapse.clone().css('display', 'block');
                $taskDetails.append($clone);
                updateProgressBars($taskDetails);
                toggleNoTasksPlaceholder();
                toggleNoCompletedTasksPlaceholder();
                showMessage(response.message, true);
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
                    const $taskId = form.find('input[name="task_id"]').val();
                    const $taskDetails = $('#taskDetails');
                    if ($taskDetails.find('input[name="task_id"]').val() === $taskId) {
                        $taskDetails.addClass('d-none');
                    }

                    toggleNoTasksPlaceholder();
                    toggleNoCompletedTasksPlaceholder();
                    initTaskViewer();
                } else {
                    showMessage('Could not delete task.', false);
                }
            },
            error: function () {
                showMessage('Server error. Try deleting task.', false);
            }
        });
    });

    $(document).on('click', '.edit-comment-btn', function () {
        const item = $(this).closest('.comment-item');
        item.find('.comment-view').addClass('d-none');
        item.find('.comment-edit-form').removeClass('d-none');
    });

    $(document).on('click', '.cancel-edit-comment-btn', function () {
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
                    form.trigger('reset');
                } else {
                    form.find('.form_errors').html(response.item_html);
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
    $(document).on('click', '.editable-field', function () {
        const $wrapper = $(this).closest('.field-wrapper');
        const $form = $wrapper.find('.edit-form');
        $(this).hide();
        $form.css('display', 'inline-block');
        $form.find('[name]').focus();
    });

    $(document).on('click', '.cancel-btn', function () {
        const $wrapper = $(this).closest('.field-wrapper');
        $wrapper.find('.edit-form').hide();
        $wrapper.find('.editable-field').show();
    });

    $(document).on('click', '.confirm-btn', function (e) {
        e.preventDefault();

        const $wrapper = $(this).closest('.field-wrapper');
        const $form = $wrapper.find('.edit-form');

        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function (response) {
                if (response.success) {
                    const taskId = $form.find('input[name="task_id"]').val();
                    const accordionItem = document.getElementById(`task-InProgress${taskId}`) || document.getElementById(`task-Done${taskId}`);
                    $(accordionItem).replaceWith(response.item_html);
                    showMessage(response.message, true);
                    $wrapper.find('.edit-form').hide();
                    $wrapper.find('.editable-field').show();
                    const $taskDetails = $('#taskDetails');
                    const $taskList = $('#mainContent');
                    $taskDetails.removeClass('d-none').empty();
                    $taskList.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
                    $taskDetails.addClass('col-12 col-lg-6');
                    const $accordionCollapse = $(response.item_html).find('.accordion-collapse').first();
                    const $clone = $accordionCollapse.clone().css('display', 'block');
                    $taskDetails.append($clone);
                    updateProgressBars($taskDetails);

                } else {
                    $wrapper.find('.form_errors').html(response.item_html);
                    showMessage(response.message, false);
                }
            },
            error: function () {
                showMessage('Server error. Could not update task.', false);
            }
        });
    });


    function toggleNoComments($container) {
        const $commentList = $container.find('.commentList');
        const hasComments = $commentList.find('.comment-item').length > 0;
        if (!hasComments) {
            $commentList.empty();
        }
    }


    function toggleNoTasksPlaceholder() {
        const $accordion = $('#accordionInProgress');
        const hasItems = $accordion.children('.accordion-item').length > 0;
        if (hasItems) {
            $('#no-tasks-placeholder').hide();
        } else {
            $('#no-tasks-placeholder').show();
        }
    }

    function toggleNoCompletedTasksPlaceholder() {
        const $accordion = $('#accordionDone');
        const hasItems = $accordion.children('.accordion-item').length > 0;
        console.log($accordion.children('.accordion-item').length);
        console.log($accordion.children('.accordion-item'));
        if (hasItems) {
            $('#no-completed-tasks-placeholder').hide();
        } else {
            $('#no-completed-tasks-placeholder').show();
        }
    }

    $(function () {
        const hash = window.location.hash;
        if (hash.indexOf('#task-') === 0) {
            const taskId = hash.replace('#task-', '');
            const el = document.getElementById(`task-InProgress${taskId}`) ||
                document.getElementById(`task-Done${taskId}`);
            const $item = $(el);              // <-- вот здесь оборачиваем
            $item.find('.accordion-button').trigger('click');
            history.replaceState(
                null,
                document.title,
                window.location.pathname + window.location.search
            );
        }
    });

});