
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin

from schedule.models import Task, TaskComment


class ScheduleMixin(FormMixin):
    def response(self, message, item_html, success, **extra):
        base = {'success': success, 'message': message, 'item_html': item_html}
        base.update(extra)
        return base

    def render_task(self, request, task, type=None):
        return render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': type},
                                request=request)

    def render_errors(self, request, form):
        return render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)

    def render_comment(self, request, comment):
        return render_to_string('schedule/includes/comment_item.html', context={'comment': comment}, request=request)

    def get_task(self, request):
        return Task.objects.get(id=request.POST.get('task_id'))

    def get_comment(self, request):
        return TaskComment.objects.get(id=request.POST.get('comment_id'))


class JsonFormMixin(FormMixin):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        raise NotImplementedError("You must override form_valid")

    def form_invalid(self, form):
        raise NotImplementedError("You must override form_invalid")
