from __future__ import absolute_import, unicode_literals

from allauth.account.forms import LoginForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout


class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CrispyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'hidden'
        self.helper.field_class = 'col-xs-12 col-sm-12 col-md-12 col-lg-8'
        self.helper.layout = Layout(
            'login',
            'password',
            Field('remember', wrapper_class='togglebutton sessionpersist'),
        )
