$(document).ready(function () {
    toggleNoDaySummary();
    toggleNoWeekSummary();
    function initTaskViewer() {
        const $mainContent = $('#mainContent');
        const $summaryDetails = $('#summaryDetails');

        $(document).off('click.task-viewer').on('click.task-viewer', '.toggle-summary', function () {
            const $item = $(this).closest('.accordion-item');
            const $accordionCollapse = $item.children('.accordion-collapse');


            $summaryDetails.removeClass('d-none').empty();
            $mainContent.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
            $summaryDetails.addClass('col-12 col-lg-6');

            const $clone = $accordionCollapse.clone().css('display', 'block');
            $summaryDetails.append($clone);

        });
    }



    initTaskViewer();

    $(document).on('click', '.accordion-toggle', function () {
        const target = $($(this).data('target'));
        const $this = $(this);
        if (target.length) {
            target.slideToggle(200);
            $this.toggleClass('open');
        }
    });


    $(document).on('click', '.close-task-btn', function () {
        const $taskDetails = $('#summaryDetails');
        const $taskList = $('#mainContent');

        $taskDetails.addClass('d-none').empty();
        $taskList.removeClass('col-lg-5').addClass('col-lg-8 col-xxl-6');
        $taskDetails.removeClass('col-12 col-lg-6');
    });


    $('.generate-btn').on('submit', function (e) {
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
                form.trigger('reset')

                form.find('.form_errors').empty();
                showMessage(response.message, true);
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });

    });

    $('.delete-summary-form').on('submit', function (e){
        e.preventDefault();
        const form = $(this);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                form.find('.form_errors').empty();
                showMessage(response.message, true);
                let item = form.closest('.accordion-item')
                let accordion = item.closest('.analysis-summary')
                item.remove();
                toggleNoDaySummary();
                toggleNoWeekSummary();
            },
            error: function () {
                showMessage('Server error. Try again later.', false);
            }
        });
    });

    function toggleNoDaySummary() {
        const $accordion = $('#day-analysis').find('.analysis-summary');

        const hasItems = $accordion.children('.accordion-item').length > 0;
        if (hasItems) {
            $('#no-day-analysis-summary').hide();
        } else {
            $('#no-day-analysis-summary').show();
        }
    }

    function toggleNoWeekSummary() {
        const $accordion = $('#week-analysis').find('.analysis-summary');
        console.log($accordion);
        const hasItems = $accordion.children('.accordion-item').length > 0;
        if (hasItems) {
            $('#no-week-analysis-summary').hide();
        } else {
            $('#no-week-analysis-summary').show();
        }
    }

});