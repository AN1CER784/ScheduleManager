from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin




class CacheMixin:
    def find_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)
        if not data:
            data = query
            cache.set(cache_name, data, cache_time)
        return data

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

class CommonFormMixin:
    def response(self, message, item_html, success, **extra):
        base = {'success': success, 'message': message, 'item_html': item_html}
        base.update(extra)
        return base

    def render_errors(self, request, form, project=None):
        return render_to_string(template_name='tasks/includes/form_errors.html', context={'form': form, 'project': project}, request=request)
