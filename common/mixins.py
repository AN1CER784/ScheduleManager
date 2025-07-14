from typing import Protocol, Any, Type

from typing import Union
from django.core.cache import cache
from django.db.models import Model, QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin

from projects.models import Project


class HasRequest(Protocol):
    request: HttpRequest


class SessionProtocol(HasRequest):
    def get_session_key(self) -> str:
        ...

    def assign_owner(self, instance: Model):
        ...

    def get_owner_filter(self, model: Model, via: bool = None):
        ...


class RequestFormKwargsMixin(FormMixin):
    def get_form_kwargs(self: HasRequest) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CacheMixin:
    @staticmethod
    def find_cache(query: Union[QuerySet, Model], cache_name: str, cache_time: int) -> QuerySet:
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
    @staticmethod
    def response(message: str, item_html: str, success: bool, **extra: Any) -> dict:
        base = {'success': success, 'message': message, 'item_html': item_html}
        base.update(extra)
        return base

    @staticmethod
    def render_errors(request, form, project: Project | None = None):
        return render_to_string(template_name='includes/form_errors.html', context={'form': form, 'project': project},
                                request=request)


class SessionMixin:
    def get_session_key(self: SessionProtocol):
        if not self.request.session.session_key:
            self.request.session.save()
        return self.request.session.session_key

    def assign_owner(self: SessionProtocol, instance: Model) -> Model:
        if self.request.user.is_authenticated:
            instance.user = self.request.user
        else:
            instance.session_key = self.get_session_key()
        instance.save()
        return instance

    def get_owner_filter(self: SessionProtocol, model: Type[Model], via: str | None = None):
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
