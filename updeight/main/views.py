from __future__ import absolute_import, unicode_literals

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'
