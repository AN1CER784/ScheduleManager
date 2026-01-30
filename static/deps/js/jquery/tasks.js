$(document).ready(function () {
    const board = $('.kanban-board');
    const kanbanUrl = board.data('kanban-url');
    const detailUrl = board.data('detail-url');
    const moveUrl = board.data('move-url');
    const detailPanel = $('#taskDetails');
    const filterForm = $('#kanban-filters');

    function getCSRFToken() {
        return $('input[name="csrfmiddlewaretoken"]').first().val();
    }

    function buildFilterParams() {
        const params = filterForm.serializeArray();
        const query = new URLSearchParams();
        params.forEach(item => {
            if (item.value !== '') {
                query.append(item.name, item.value);
            }
        });
        return query;
    }

    function updateQueryParams() {
        const query = buildFilterParams().toString();
        const newUrl = `${window.location.pathname}${query ? `?${query}` : ''}`;
        window.history.replaceState({}, '', newUrl);
    }

    function renderDetail(html) {
        detailPanel.removeClass('d-none').html(html);
    }

    function closeDetail() {
        detailPanel.addClass('d-none').empty();
    }

    function loadDetail(taskId) {
        $.ajax({
            type: 'GET',
            url: detailUrl,
            data: { task_id: taskId },
            success: function (response) {
                if (response.success) {
                    renderDetail(response.detail_html);
                } else {
                    showMessage(response.message || 'Could not load task.', false);
                }
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });
    }

    function updateColumnCount(status, delta, setTo) {
        const column = $(`.kanban-column[data-status="${status}"]`);
        const countEl = column.find('.kanban-count');
        if (setTo !== undefined) {
            countEl.text(setTo).attr('data-count', setTo);
            return;
        }
        const current = parseInt(countEl.attr('data-count'), 10) || 0;
        const next = Math.max(current + delta, 0);
        countEl.text(next).attr('data-count', next);
    }

    function buildOrder($list) {
        return $list.children('.kanban-card').map(function () {
            return $(this).data('task-id');
        }).get();
    }

    function loadColumn($list, reset) {
        const status = $list.data('status');
        const hasNext = $list.data('has-next');
        let page = parseInt($list.data('page'), 10) || 1;
        if (!reset && !hasNext) {
            return;
        }
        if ($list.data('loading')) {
            return;
        }
        $list.data('loading', true);
        if (reset) {
            page = 1;
            $list.data('page', 1);
        }
        const query = buildFilterParams();
        query.append('column_status', status);
        query.set('page', page);
        query.set('page_size', 20);
        $.ajax({
            type: 'GET',
            url: kanbanUrl,
            data: query.toString(),
            success: function (response) {
                if (!response.success) {
                    return;
                }
                if (reset) {
                    $list.find('.kanban-card').remove();
                }
                const html = $(response.items_html.trim());
                $list.find('.kanban-sentinel').before(html);
                $list.data('has-next', response.has_next);
                if (response.has_next) {
                    $list.data('page', response.next_page);
                }
                updateColumnCount(status, 0, response.total);
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            },
            complete: function () {
                $list.data('loading', false);
            }
        });
    }

    function refreshBoard() {
        updateQueryParams();
        $('.kanban-list').each(function () {
            loadColumn($(this), true);
        });
    }

    filterForm.on('submit', function (e) {
        e.preventDefault();
        refreshBoard();
    });

    $(document).on('change', '#kanban-filters select, #kanban-filters input[type="checkbox"]', function () {
        refreshBoard();
    });

    $(document).on('click', '.kanban-open-btn', function () {
        loadDetail($(this).data('task-id'));
    });

    $(document).on('click', '.close-task-btn', function () {
        closeDetail();
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
                    form.find('.form_errors').html(response.item_html);
                    return showMessage(response.message, false);
                }
                form.find('.form_errors').empty();
                const $card = $(response.item_html.trim());
                const $list = $('.kanban-list[data-status="NEW"]');
                $list.prepend($card);
                updateColumnCount('NEW', 1);
                if (response.detail_html) {
                    renderDetail(response.detail_html);
                }
                showMessage(response.message, true);
                form.trigger('reset');
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });
    });

    $(document).on('submit', '.status-change-form', function (e) {
        e.preventDefault();
        const form = $(this);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (!response.success) {
                    return showMessage(response.message, false);
                }
                const taskId = form.find('input[name="task_id"]').val();
                const $oldCard = $(`.kanban-card[data-task-id="${taskId}"]`);
                const oldStatus = $oldCard.data('status');
                const $newCard = $(response.item_html.trim());
                $oldCard.remove();
                $(`.kanban-list[data-status="${response.status}"]`).prepend($newCard);
                updateColumnCount(oldStatus, -1);
                updateColumnCount(response.status, 1);
                if (response.detail_html) {
                    renderDetail(response.detail_html);
                }
                showMessage(response.message, true);
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });
    });

    $(document).on('submit', '.send-result-form', function (e) {
        e.preventDefault();
        const form = $(this);
        const $container = form.closest('[id^="result"]');
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (!response.success) {
                    form.find('.form_errors').html(response.item_html);
                    return showMessage(response.message, false);
                }
                form.find('.form_errors').empty();
                const resultList = $container.find('.resultList');
                resultList.find('.no-results').remove();
                resultList.append(response.item_html);
                showMessage(response.message, true);
                form.trigger('reset');
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
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
                    form.find('.form_errors').html(response.item_html);
                    return showMessage(response.message, false);
                }
                form.find('.form_errors').empty();
                const commentList = $container.find('.commentList');
                const dateId = response.comment_date;
                const dividerId = '#divider' + dateId;
                if (commentList.find(dividerId).length === 0) {
                    commentList.append(response.divider_html);
                }
                commentList.append(response.item_html);
                showMessage(response.message, true);
                form.trigger('reset');
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
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
                    showMessage(response.message, true);
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
                    const $item = form.closest('.comment-item');
                    const $container = $item.closest('.commentList');
                    const $divider = $item.prevAll('.textDivider').first();
                    $item.remove();

                    if ($divider.length) {
                        const $nextDivider = $divider.nextAll('.textDivider').first();
                        const $between = $nextDivider.length ? $divider.nextUntil($nextDivider, '.comment-item') : $divider.nextAll('.comment-item');
                        if ($between.length === 0) {
                            $divider.remove();
                        }
                    }

                    showMessage(response.message, true);
                } else {
                    showMessage('Could not delete comment.', false);
                }
            },
            error: function () {
                showMessage('Server error. Try deleting comment.', false);
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
                if (!response.success) {
                    return showMessage('Could not delete task.', false);
                }
                const taskId = form.find('input[name="task_id"]').val();
                const $card = $(`.kanban-card[data-task-id="${taskId}"]`);
                if ($card.length) {
                    const status = $card.data('status');
                    $card.remove();
                    updateColumnCount(status, -1);
                } else {
                    refreshBoard();
                }
                if (detailPanel.find(`[data-task-id="${taskId}"]`).length) {
                    closeDetail();
                }
                showMessage(response.message, true);
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
        $form.css('display', 'block');
        $form.find('[name]').first().focus();
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
                if (!response.success) {
                    $wrapper.find('.form_errors').html(response.item_html);
                    return showMessage(response.message, false);
                }
                const taskId = $form.find('input[name="task_id"]').val();
                const $oldCard = $(`.kanban-card[data-task-id="${taskId}"]`);
                const $newCard = $(response.item_html.trim());
                $oldCard.replaceWith($newCard);
                if (response.detail_html) {
                    renderDetail(response.detail_html);
                }
                showMessage(response.message, true);
            },
            error: function () {
                showMessage('Server error. Could not update task.', false);
            }
        });
    });


    $('.kanban-list').each(function () {
        const list = this;
        const sentinel = list.querySelector('.kanban-sentinel');
        if (!sentinel) {
            return;
        }
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    loadColumn($(list), false);
                }
            });
        }, { root: list, rootMargin: '200px' });
        observer.observe(sentinel);
    });

    let dragState = null;

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.kanban-card:not(.dragging)')];
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset, element: child };
            }
            return closest;
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    $(document).on('dragstart', '.kanban-card', function (e) {
        const $card = $(this);
        $card.addClass('dragging');
        const $list = $card.closest('.kanban-list');
        dragState = {
            taskId: $card.data('task-id'),
            sourceStatus: $list.data('status'),
            sourceList: $list,
        };
        e.originalEvent.dataTransfer.effectAllowed = 'move';
    });

    $(document).on('dragend', '.kanban-card', function () {
        $(this).removeClass('dragging');
    });

    $('.kanban-list').each(function () {
        const list = this;
        list.addEventListener('dragover', function (e) {
            e.preventDefault();
            const afterElement = getDragAfterElement(list, e.clientY);
            const dragging = document.querySelector('.dragging');
            if (!dragging) {
                return;
            }
            if (afterElement == null) {
                list.insertBefore(dragging, list.querySelector('.kanban-sentinel'));
            } else {
                list.insertBefore(dragging, afterElement);
            }
        });

        list.addEventListener('drop', function () {
            if (!dragState) {
                return;
            }
            const $targetList = $(list);
            const targetStatus = $targetList.data('status');
            const targetOrder = buildOrder($targetList);
            const sourceOrder = dragState.sourceStatus === targetStatus ? targetOrder : buildOrder(dragState.sourceList);
            const payload = {
                task_id: dragState.taskId,
                new_status: targetStatus,
                target_order: targetOrder,
                source_order: dragState.sourceStatus === targetStatus ? [] : sourceOrder,
            };

            fetch(moveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify(payload),
            }).then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        refreshBoard();
                        showMessage(data.message || 'Status change not allowed', false);
                        return;
                    }
                    if (dragState.sourceStatus !== targetStatus) {
                        updateColumnCount(dragState.sourceStatus, -1);
                        updateColumnCount(targetStatus, 1);
                        const card = document.querySelector(`.kanban-card[data-task-id="${dragState.taskId}"]`);
                        if (card) {
                            card.setAttribute('data-status', targetStatus);
                            card.dataset.status = targetStatus;
                        }
                        if (detailPanel.length && detailPanel.find(`[data-task-id="${dragState.taskId}"]`).length) {
                            loadDetail(dragState.taskId);
                        }
                    }
                })
                .catch(() => {
                    refreshBoard();
                    showMessage('Server error. Try again later.', false);
                })
                .finally(() => {
                    dragState = null;
                });
        });
    });
});
