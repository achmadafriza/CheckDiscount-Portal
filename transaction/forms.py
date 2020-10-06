from django import forms

class CheckDiscountForm(forms.Form):
    ammount = forms.IntegerField(min_value=10000, max_value=20000000)
    time = forms.DateTimeField()