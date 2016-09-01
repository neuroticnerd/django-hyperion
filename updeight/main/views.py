from __future__ import absolute_import, unicode_literals

from django.views.generic.base import TemplateView

from .forms import CrispyLoginForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = CrispyLoginForm()
        return context
