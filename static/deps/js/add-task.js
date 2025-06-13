document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('enable_due_fields');
    const dueFields = document.getElementById('due-fields');
    const dueDate = document.getElementById('id_due_date');
    const dueTime = document.getElementById('id_due_time');

    function updateVisibility() {
        if (toggle.checked) {
            dueFields.style.display = 'flex';
            dueDate.required = true;
            dueTime.required = true;
        } else {
            dueFields.style.display = 'none';
            dueDate.value = '';
            dueTime.value = '';
            dueDate.required = false;
            dueTime.required = false;
        }
    }

    toggle.addEventListener('change', updateVisibility);
    updateVisibility();
});