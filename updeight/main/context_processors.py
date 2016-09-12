from __future__ import absolute_import, unicode_literals

from django.urls import reverse


def login_context(request):
    context = {'render_login_modal': True}
    if reverse('account_login') in request.path:
        context['render_login_modal'] = False
    return context
