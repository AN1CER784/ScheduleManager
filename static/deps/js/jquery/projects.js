$(document).ready(function () {
    toggleNoProjectsPlaceholder();
    $(document).on('click', '.edit-proj-btn', function () {
        const item = $(this).closest('.project-card');
        item.find('.project-name').addClass('d-none');
        item.find('.proj-edit-form').removeClass('d-none');
    });

    $(document).on('click', '.cancel-proj-edit-btn', function () {
        const item = $(this).closest('.project-card');
        item.find('.proj-edit-form').addClass('d-none');
        item.find('.project-name').removeClass('d-none');
    });


    $(document).on('submit', '.proj-edit-form', function (e) {
        e.preventDefault();
        const form = $(this);
        const item = form.closest('.project-card');

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    const $newItem = $(response.item_html);
                    item.replaceWith($newItem);
                    form.addClass('d-none');
                    item.find('.project-name').removeClass('d-none');
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

    function toggleNoProjectsPlaceholder() {
        const $container = $('#projectsContainer');
        const hasProjects = $container.find('.project-card').length > 0;
        if (hasProjects) {
            $('#no-proj-placeholder').hide();
        } else {
            $('#no-proj-placeholder').show();
        }
    }
});