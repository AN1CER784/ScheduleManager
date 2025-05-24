$(document).ready(function () {
    function initTaskViewer() {
        const $mainContent = $('#mainContent');
        const $summaryDetails = $('#summaryDetails');

        $(document).off('click.task-viewer').on('click.task-viewer', '.toggle-summary', function () {
            const $item = $(this).closest('.accordion-item');
            const $accordionCollapse = $item.children('.accordion-collapse');


            $summaryDetails.removeClass('d-none').empty();
            $mainContent.removeClass('col-lg-6').addClass('col-lg-5');
            $summaryDetails.addClass('col-12 col-lg-6');

            const $clone = $accordionCollapse.clone().css('display', 'block');
            $summaryDetails.append($clone);

            // const $analysisSummary = $(this).closest('.analysis-summary');
            // const $summaryBody = $analysisSummary.find('.summary-body');
            // $summaryDetails.removeClass('d-none').empty();
            // $mainContent.removeClass('col-lg-6').addClass('col-lg-5');
            // $summaryDetails.addClass('col-12 col-lg-6');
            //
            // const $clone = $summaryBody.clone().css('display', 'block');
            // $summaryDetails.append($clone);
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
        $taskList.removeClass('col-lg-5').addClass('col-lg-6');
        $taskDetails.removeClass('col-12 col-lg-6');
    });
});