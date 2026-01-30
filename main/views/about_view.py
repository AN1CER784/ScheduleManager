from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from common.mixins import CacheMixin
from main.models import Page


class AboutView(CacheMixin, TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('About page')
        query = Page.objects.get(key='about')
        context['content'] = self.find_cache(query, 'content_about', 60 * 60)
        return context
