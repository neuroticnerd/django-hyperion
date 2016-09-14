from __future__ import absolute_import, unicode_literals

from allauth.account.forms import LoginForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CrispyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-xs-3 col-sm-2 col-md-2 col-lg-1'
        self.helper.field_class = 'col-xs-9 col-sm-10 col-md-10 col-lg-11'
        self.helper.layout = Layout(
            'login',
            'password',
            Field('remember', wrapper_class='togglebutton sessionpersist'),
        )

    def no_labels(self):
        self.helper.label_class = 'hidden'
        self.helper.field_class = 'col-xs-12 col-sm-12 col-md-12 col-lg-12'
