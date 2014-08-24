from django import forms
from django.forms import ModelForm

from expenses.models import Expense


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category']

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.iteritems():
            field.widget.attrs['class'] = 'form-control'
