$(document).ready(function () {
    function initTaskViewer() {
        const $mainContent = $('#mainContent');
        const $taskList = $('#tasksList');

        $(document).off('click.task-list-viewer').on('click.task-list-viewer', '.toggle-tasks-list', function () {
            const $item = $(this).closest('.calendar-day').next('.tasks-list');
            console.log($item);
            $taskList.removeClass('d-none').empty();
            $mainContent.removeClass('col-lg-8 col-xxl-6').addClass('col-lg-5');
            $taskList.addClass('col-12 col-lg-6');

            const $clone = $item.clone().css('display', 'block');
            $taskList.append($clone);

        });
    }
    initTaskViewer();

     $(document).on('click', '.close-task-btn', function () {
        const $tasksList = $('#tasksList');
        const $taskList = $('#mainContent');

        $tasksList.addClass('d-none').empty();
        $taskList.removeClass('col-lg-5').addClass('col-lg-8 col-xxl-6');
        $tasksList.removeClass('col-12 col-lg-6');
    });
});