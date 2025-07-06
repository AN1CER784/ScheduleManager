from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin


class RequestFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


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
        return render_to_string(template_name='includes/form_errors.html', context={'form': form, 'project': project},
                                request=request)


class SessionMixin:
    def get_session_key(self):
        if not self.request.session.session_key:
            self.request.session.save()
        return self.request.session.session_key

    def assign_owner(self, instance):
        if self.request.user.is_authenticated:
            instance.user = self.request.user
        else:
            instance.session_key = self.get_session_key()
        instance.save()
        return instance

    def get_owner_filter(self, model, via=None):
        if self.request.user.is_authenticated:
            field = 'user'
            value = self.request.user
        else:
            field = 'session_key'
            value = self.get_session_key()

        if via:
            lookup = f"{via}__{field}"
        else:
            lookup = field

        return model.objects.filter(**{lookup: value})
