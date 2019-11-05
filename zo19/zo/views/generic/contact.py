from .select_multi_form import SelectMultiFormView
from zo.forms.generic import GeneralContactForm

from datetime import datetime

class GenericContactView(SelectMultiFormView):

    title = 'General Contact'
    forms = [GeneralContactForm]
    form_type = 'Contact'
    layout = 'zo/public'
