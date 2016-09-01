from __future__ import absolute_import, unicode_literals

from allauth.account.forms import LoginForm

from crispy_forms.helper import FormHelper


class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CrispyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.label_class = 'hidden'
